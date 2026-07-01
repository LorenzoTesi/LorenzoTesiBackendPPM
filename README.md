Event Management System
studente: Lorenzo Tesi matricola: 7149989

Full-stack Web application
Framework usato: Django
L'applicazione è un gestore di eventi. Estistono due tipi di profili: partecipante e organizzatore.
Partecipante dopo il login può cercare gli eventi, vederne i dettagli ed iscriversi/disiscriversi, può inoltre cambiare
le informazioni (username, nome, cognome, mail) del proprio profilo e cancellarlo.
Organizzatore può o accedere dalla schermata di login dei partecipanti e comportarsi come un partecipante
(con la sola differenza che non può iscriversi ad eventi da lui organizzati), oppure può accedere tramite la pagina
di login degli organizzatori. Da qui può cercare e vedere i dettagli gli eventi da lui creati ( ed eventualmente
modificarli o cancellarli), può modificare il proprio profilo; può scegliere di promuovere un utente partecipante
già esistente ad organizzatore, oppure creare un profilo organizzatore nuovo ( la pagina di registrazione può
solo creare dei partecipanti).


superuser: admin, password: admin123

profili organizzatore:
username: Organizzatore1 , pw: Delfino03
nome: Mario , cognome: Rossi , email: mario.rossi@gmail.com

username: Organizzatore2 , pw: Scimmia03
nome: Luigi , cognome: Verdi , email : luigi.verdi@gmail.com

profili partecipante: 
username: Partecipante1 , pw: Pellicano03
nome: Elena , cognome: Mori , email: elena.mori@gmail.com

username: Partecipante2, pw: Cammello03

username: Partecipante3 , pw: Pinguino03

username: Partecipante4, pw: Balena03

sono presenti 3 eventi: spettacolo di magia di Fabio Bianchi, concerto di Mario Rossi, spettacolo di standup di Marco Testuya.
Rispettivamente con 3,3 e 5 posti di capienza, i primi 3 partecipanti sono già tutti
iscritti allo spettacolo di magia, inoltre Partecipante3 è già iscritto allo spettacolo di stand up, Partecipante4 non è iscritto a nulla.


URL : LorenzoTesi1.pythonanywhere.com