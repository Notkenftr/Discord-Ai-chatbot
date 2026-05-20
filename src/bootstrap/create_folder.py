import os

def create_folder():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
    try:
        os.makedirs(
            os.path.join(root,"libs"),
            exist_ok=True)
        os.makedirs(
            os.path.join(root,"data"),
            exist_ok=True
        )
        os.makedirs(
            os.path.join(root,"logs"),
            exist_ok=True
        )
    except OSError as e:
        raise e