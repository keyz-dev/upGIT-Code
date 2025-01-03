from app.services.github import GithubUtililty
from app.utils.decorator import global_exception_handler
from ..models.user import User as user_model
from ..schema.user import UserCreate
from ..crud import user as user_crud
from ..utils.constants import logger
import os
from app.controllers import remote_repo as remote_repo_controller


class UserAuthentication():
    def __init__(self):
        pass
    @global_exception_handler
    def handle_acc_creation(self, user_object):
        """Handle user registration and remote repo creation"""
        self.user_object = user_object
        status, user = self.register()
        if not status:
            return False, user
        
        github_obj = GithubUtililty()
        repo_name = 'upGIT' + '_' + user.name + '_' + str(user.id)
        created_repo = github_obj.create_repo(repo_name=repo_name)
        repo_object = {
            'name': created_repo.name,
            'user_id': user.id,
            'url': created_repo.html_url,
            'clone_url': created_repo.clone_url
        }
        """Save the repo to the database"""
        saved_repo = remote_repo_controller.save(repo_object)
        if saved_repo:
            logger.info(f'Successfully created remote repository for {created_repo.name} and saved it to the database')
            return True, user
        else:
            return False, 'Failed to create remote repository'
    @global_exception_handler
    def register(self):
        """Validate the user information"""
        user = UserCreate(**self.user_object)
        user = user.dict()
        
        """remove the confirm password_field and Insert the user"""
        user.pop('confirm_password')
        model_object = user_model(**user)
        
        """hash the password field"""
        model_object.set_password()
        
        """Insert the new user"""
        created_user = user_crud.create(user=model_object)
        
        # write the user id to flat file
        with open(os.path.join(os.path.dirname(__file__), 'user_id.txt'), 'w') as f:
            f.write(str(created_user.id))
        logger.info(f"User created without fault \n{created_user}")
        return True, created_user
            
    @global_exception_handler
    def login(self, user_object):
        user = user_crud.get_by_email(email=user_object["email"])
        if user:
            if user.check_password(user_object["password"]): 
                logger.info(f"User, {user.name} logged in successfully")
                return True, user
        logger.error(f"Incorrect email or password")
        return False, "Incorrect email or password"
