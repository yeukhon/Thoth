from user import User
from document import Document, DocumentManager
from md5 import new
from time import time


if __name__ == "__main__":
    # Debugging:
    verbose = False

    # Start with a guest user.
    guest = User(1)

    # The usergroup for regular users.
    RU = 2

    # Apply to the system.
    guest.manage_DB.insert_info('application', insert={
        'username': 'Gary',
        'password': new('eevee').hexdigest(),
        'email': 'GOak@pokemon.com',
        'usergroup': RU,
        'content': 'Ash is a loser.',
        'time': time(),
        'status': 0}, verbose=verbose)

    # Default settings for new users.
    infraction = 0

    # Add a new user.
    guest.manage_DB.insert_info('user', insert={
        'username': 'Ash',
        'password': new('pika').hexdigest(),
        'email': 'AKetchum@pokemon.com',
        'usergroup': RU,
        'infraction': infraction}, verbose=verbose)
    # Create an instance of the User class for the newly created user.
    ash = User(username='Ash')

    root = 1
    # Add a folder to the dB at the root directory.
    ash.manage_DB.insert_info('directory', insert={
        'name': 'Team',
        'parent_dir': root}, verbose=verbose)
    # Get the 'id' of the newly created directory.
    teamid = ash.manage_DB.get_info('directory', where={
        'name': 'Team'}, verbose=verbose)[0]['id']
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
    ash.manage_DB.insert_info('document', insert={
        'name': 'Pikachu',
        'parent_dir': teamid,
        'owner': ash.info['id'],
        'infraction': infraction,
        'last_mod_user': last_mod_user,
        'last_mod_time': last_mod_time,
        'size': size}, verbose=verbose)
    # Get the 'id' of the newly created document.
    pikaid = ash.manage_DB.get_info('document', where={
        'name': 'Pikachu', 'parent_dir': teamid}, verbose=verbose)[0]['id']
    # Create the newly inserted document at the directory 'Team'.
    manage_Docs.create_document(pikaid, teamid)
    # Create an instance of the Document class for the newly created document.
    pika = Document(pikaid)

    # Leave a comment on the document.
    ash.manage_DB.insert_info('comment', insert={
        'docid': pika.info['id'],
        'userid': ash.info['id'],
        'content': 'Pikachu use Thunderbolt!',
        'time': time()}, verbose=verbose)
    ash.manage_DB.insert_comment('comment', insert={
        'docid': pika.info['id'],
        'userid': ash.info['id'],
        'content': 'Pikachu use Quick Attack!',
        'time': time()}, verbose=verbose)

    # The 'id' of the admin user.
    adminid = 2
    # The default setting for new invitations.
    pending = 0

    # Invite Admin to the document.
    ash.manage_DB.insert_info('invitation', insert={
        'docid': pika.info['id'],
        'userid_from': ash.info['id'],
        'userid_to': adminid,
        'content': 'Train my Pikachu.',
        'time': time(),
        'status': pending}, verbose=verbose)

    # Complain about the document.
    ash.manage_DB.insert_info('complaint', insert={
        'docid': pika.info['id'],
        'userid': ash.info['id'],
        'content': 'Pikachu is not obeying me!',
        'time': time(),
        'status': pending}, verbose=verbose)

    # Index the document.
    manage_Docs.index_document(pika.info['id'])

    # Search the document.
    res = manage_Docs.manage_Indx.search('please')
    for i in res:
        print i['branch_word'], i['line'], i['column']
