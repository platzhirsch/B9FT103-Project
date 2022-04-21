import typer
from verifyAndCheck import checkFile, verifyFile, addCollaborators, deleteCollaborators


app = typer.Typer()

@app.command()
def updatehash(filename: str):
   verifyFile(filename)

@app.command()
def checkhash(filename: str):
    checkFile(filename)

@app.command()
def addCollaborator(adress: str, name: str):
    addCollaborators(adress, name)

@app.command()
def deleteCollaborator(adress: str):
    deleteCollaborators(adress)


if __name__ == "__main__":
    app()
