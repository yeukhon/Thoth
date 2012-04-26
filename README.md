Thoth
=====

Csc 332: Text Editor

A smart multi-user document system
Spring, 2012

In this semester the term project is a smart text editing system shared by a group of users.

User management subsystem:
1. This system has super-users who manage user accounts and documents.
2. A user is treated as a visitor if s/he does not have an account or didn’t log in yet.
3. To become an ordinary user the visitor should file an application that is processed (accept or deny) by a super-user.
4. There are three types of users for each document: owners, members and visitors: An owner, who must be an ordinary user of the system, initiates a new document and invites other ordinary users as members who can either deny or accept the invitation.
5. Owners and members can freely update (only one can update at any one time) and comment on the document while visitors can only browse and comment on it. Comments of one document are saved in a text file and displayed in a different window/region from the document.
6. All browsers of a document can submit complaints to the owner or the super-users who will take actions with feedback to the one who complained.
7. Any document that was complained more than three times to the super-users will be suspended so that no one can see it any longer unless the super-users want to restore it. The user account is closed is s/he is the owner of more than two suspended documents.

Document management subsystem:
1. Editing: owners/members can open, edit, save, close, redo/undo, search and/or replace (Regex supported);
2. Appearances: provide choices for line number, font size, background/foreground color, menu bars/icons of functionalities;
3. recent file history: who, what, where and when generated automatically after every updating, only the recent 3 updates are saved;
4. Smart features: spell checking (incorrect words highlighted automatically), each member can add new words to his/her own dictionary when changing the incorrect spellings, the system should provide up to 5 reasonable suggestions for every wrong words; the owner’s dictionary is the master one shared by other members;
5. Indexing and searching: two UI items accordingly should be provided; the index of words after stemming and stop word cleansing should be provided for each document, each word is indexed by its line number in the document and location in the line, e.g., in document a.txt, the index “ccny 10 15” indicates that word ccny occurs on line 10 at location 15; any user (owner, member and visitor) can search documents based on one word or word sequences in quotes, e.g., “city college”; and find similar documents for a given document based on word indexes (your creative feature can be applied here to render it more intelligent/useful/practical).

System requirements:
1. The system should be running alone application, the final working system should be able to boot and work from your submitted CD only, i.e., copy from CD to a folder in hard disk so that your system can have free read/write privilege, use of database is not permitted.
2. Each team should have at least one creative feature that is not formulated in the foregoing requirements, this creative feature account for 15% of the entire score of the final working system. Extra bonus may be given to those extremely creative features, depending on how creative/smart it is.
