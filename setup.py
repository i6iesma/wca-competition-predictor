import update_db
import subprocess
def main():
    install_requirements()
    update_db.main()


def install_requirements():
    subprocess.run(["pip install -r requirements.txt"])
    





    
