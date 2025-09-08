from app.models.moments_models import Moment
from app.schemas.moments_schema import MomentBase, MomentResponse, MomentUpdate
from app.schemas.user import GenericResponseModel
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from uuid import UUID
from datetime import datetime
from app.models.event_models import Events
from app.models.user_models import User
import os, shutil, uuid

class MomentService():
    def __init__(self, db: Session):
        self.db = db

    def GenerateResponse(self, status_code: int, message: str, data: dict = None):
        return {
            "status_code": status_code,
            "message": message,
            "data": data
        }
    
    def create_moment(self, moment_data: MomentBase, user: User, token: str, media_file: UploadFile = None):
        event = self.db.query(Events).filter(Events.id == moment_data.event_id).first()
        if user.role != "participant":
            return self.GenerateResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                message="Only participants can create moments."
            )
        if not event:
            return self.GenerateResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Event not found."
            )
        if moment_data.type in [ "image", "video"] and not media_file:
            return self.GenerateResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=f"Media file is required for moment type '{moment_data.type}'."
            )
        if moment_data.type == "text" and media_file:
            return self.GenerateResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Media file should not be provided for moment type 'text'."
            )
        
        media_url = None
        if media_file:
            file_extension = os.path.splitext(media_file.filename)[1]
            if file_extension.lower() not in [".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mov", ".avi"]:
                return self.GenerateResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Unsupported media file type."
                )
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            upload_dir = os.path.join("media", "moments")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, unique_filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(media_file.file, buffer)
            media_url = f"/static/moments/{unique_filename}"
            moment_data.media_url = media_url
        new_moment = Moment(
            id=uuid.uuid4(),
            event_id=moment_data.event_id,
            user_id=user.id,
            type=moment_data.type,
            content=moment_data.content,
            media_url=media_url,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(new_moment)
        self.db.commit()
        self.db.refresh(new_moment)
        return self.GenerateResponse(
            status_code=status.HTTP_201_CREATED,
            message="Moment created successfully.",
            data=MomentResponse.from_orm(new_moment)
        )

    def get_moments_by_event(self, event_id: UUID):
        event = self.db.query(Events).filter(Events.id == event_id).first()
        if not event:
            return self.GenerateResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Event not found."
            )
        moments = self.db.query(Moment).filter(Moment.event_id == event_id).all()
        return self.GenerateResponse(
            status_code=status.HTTP_200_OK,
            message="Moments retrieved successfully.",
            data=[MomentResponse.from_orm(moment) for moment in moments]
        )
    
    def update_moment(self, id: UUID, moment_data: MomentUpdate, user: User, token: str, media_file: UploadFile = None):
        moment = self.db.query(Moment).filter(Moment.id == id, Moment.user_id == user.id).first()
        if not moment:
            return self.GenerateResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Moment not found or you do not have permission to update it."
            )
        if moment_data.type and moment_data.type in ["image", "video"] and not media_file:
            return self.GenerateResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=f"Media file is required for moment type '{moment_data.type}'."
            )
        if moment_data.type and moment_data.type == "text" and media_file:
            return self.GenerateResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Media file should not be provided for moment type 'text'."
            )
        
        if moment_data.content is not None:
            moment.content = moment_data.content
        if moment_data.type is not None:
            moment.type = moment_data.type
        moment.updated_at = datetime.utcnow()

        if media_file:
            file_extension = os.path.splitext(media_file.filename)[1]
            if file_extension.lower() not in [".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mov", ".avi"]:
                return self.GenerateResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Unsupported media file type."
                )
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            upload_dir = os.path.join("media", "moments")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, unique_filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(media_file.file, buffer)
            moment.media_url = f"/static/moments/{unique_filename}"
            
        self.db.commit()
        self.db.refresh(moment)
        return self.GenerateResponse(
            status_code=status.HTTP_200_OK,
            message="Moment updated successfully.",
            data=MomentResponse.from_orm(moment)
        )