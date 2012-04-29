from user import User
from document import Document, DocumentManager
from md5 import new
from time import time


if __name__ == "__main__":
    # Start with a guest user.
    guest = User(1)

    # The usergroup for regular users.
    RU = 2
    # Default settings for new users.
    infraction = 0

    # Add a new user.
    guest.manage_DB.insert_user(
        'Ash', new('pika').hexdigest(), 'AKetchum@pokemon.com', RU, infraction)
    # Create an instance of the User class for the newly created user.
    ash = User(username='Ash')

    # Add a folder to the dB at the root directory.
    ash.manage_DB.insert_directory('Team')
    # Get the 'id' of the newly created directory.
    teamid = ash.manage_DB.get_directory_info(name='Team')['id']
    # Create the directory.
    team = ash.manage_Dir.create_directory(teamid)

    # Create an instance of the DocumentManager class and pass it an instance
    # of the DBManager class.
    manage_Docs = DocumentManager(ash.manage_DB)

    # Default settings for new documents.
    last_mod_user = 0
    last_mod_time = 0
    size = 0

    # Add a document to the dB at the directory 'Team'.
    ash.manage_DB.insert_document('Pikachu', teamid, ash.info['id'],
        infraction, last_mod_user, last_mod_time, size)
    # Get the 'id' of the newly created document.
    pikaid = ash.manage_DB.get_document_info(
        name='Pikachu', parent_dir=teamid)['id']
    # Create the newly inserted document at the directory 'Team'.
    manage_Docs.create_document(pikaid, teamid)
    # Create an instance of the Document class for the newly created document.
    pika = Document(pikaid)

    # Leave a comment on the document.
    ash.manage_DB.insert_comment(
        pika.info['id'], ash.info['id'], 'Pikachu use Thunderbolt!', time())
    ash.manage_DB.insert_comment(
        pika.info['id'], ash.info['id'], 'Pikachu use Quick Attack!', time())

    # The 'id' of the admin user.
    adminid = 2
    # The default setting for new invitations.
    pending = 0

    # Invite Admin to the document.
    ash.manage_DB.insert_invitation(
        pika.info['id'], ash.info['id'], adminid, 'Train my Pikachu.', time(),
        pending)

    # Complain about the document.
    ash.manage_DB.insert_complaint(
        pika.info['id'], ash.info['id'], 'Pikachu is not obeying me!', time(),
        pending)

    # Index the document.
    manage_Docs.index_document(pika.info['id'])

    # Search the document.
    res = manage_Docs.manage_Indx.search('please')
    for i in res:
        print i['branch_word'], i['line'], i['column']
