import subprocess
def main():
    install_requirements()
    import update_db
    update_db.main()


def install_requirements():
    subprocess.run(["pip install -r requirements.txt"])

main()





    
