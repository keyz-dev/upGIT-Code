import threading
from app.utils.constants import logger
from app.config.database import init_db
from app.services import pull, background_backup
from app.views.view import MainApp
from app.utils.decorator import global_exception_handler
from app.services.manage_files import organize_pull_files

def start_backup_thread():
    """Start the backup thread"""
    backup_thread = threading.Thread(target=background_backup.bg_backup())
    backup_thread.daemon = True
    backup_thread.start()

@global_exception_handler
def db_connection():
    """Initialize the database connection"""
    init_db()
    
def main():    
    db_connection()
    MainApp()
    
    
    
    