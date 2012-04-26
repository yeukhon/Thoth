from user import User, UserManager
from document import Document
from index import IndexManager


if __name__ == "__main__":
    # Start with a guest user.
    guest   = User(1)

    # Add a new user.
    RU      = 2
    ashid   = guest.manage_User.add_user(
        'Ash', 'pika', 'AKetchum@pokemon.com', RU)[1]
    ash     = User(ashid)

    # Add a folder to the dB and create it.
    rootid  = 1
    teamid  = ash.manage_Dir.add_directory('Team', rootid)[1]
    team    = ash.manage_Dir.create_directory(teamid, rootid)

    # Add a document to the dB and create it.
    pikaid  = ash.manage_Docs.add_document(
        'Pikachu', teamid, ash.info['id'], 0)[1]
    ash.manage_Docs.create_document(pikaid, teamid)
    pika    = Document(pikaid)

    # Leave a comment on the document.
    pika.insert_comment(ash.info['id'], 'Pikachu use Thunderbolt!')
    pika.insert_comment(ash.info['id'], 'Pikachu use Quick Attack!')

    # Invite Admin to the document.
    adminid = 2
    pika.insert_invitation(ash.info['id'], adminid, 'Train my Pikachu.')

    # Complaint about the document.
    pika.insert_complaint(ash.info['id'], 'Pikachu is not obeying me!')

    # Index the document.
    pika.index_document()

    # Search the document.
    res     = pika.manage_Indx.search('please')
    for i in res:
        print i['word'], i['line'], i['column']
