insert into CLIENT values(1, true),
                          (2, false),
                          (3, false),
                          (4, false),
                          (5, true),
                          (6, true),
                          (7, true),
                          (8, false),
                          (9, false),
                          (10, true),
                          (11, false),
                          (12, true);
    
insert into COURS values(1, 'Cours de saut', "Ce cours portera sur la technique de saut d'obstacle pour les débutants", "Collectif", 45), 
                           (2, 'Cours de saut', "Ce cours portera sur la technique de saut d'obstacle pour les débutants", "Individuel", 80),
                           (3, 'Initiation', "Cours d'initiation au poney ", "Individuel", 65),
                           (4, 'Initiation', "Cours d'initiation au poney ", "Collectif", 25),
                           (5, 'Cours de course', "Ce cours portera sur la course à poney", "Individuel", 65),
                           (6, 'Cours poussin', "Ce cours sera un entraînement pour la catégorie poussin", "Collectif", 35),
                           (7, 'Cours de saut', "Ce cours portera sur la technique de saut d'obstacle pour les débutants", "Collectif", 45),
                           (8, 'Cours de saut', "Ce cours portera sur la technique de saut d'obstacle pour les débutants", "Individuel", 45),
                           (9, 'Cours de saut', "Ce cours portera sur la technique de saut d'obstacle pour les débutants", "Individuel", 45),
                           (10, 'Cours de saut', "Ce cours portera sur la technique de saut d'obstacle pour les débutants", "Collectif", 45),
                           (11, 'Cours de saut', "Ce cours portera sur la technique de saut d'obstacle pour les débutants", "Individuel", 45),
                           (12, 'Cours de saut', "Ce cours portera sur la technique de saut d'obstacle pour les débutants", "Collectif", 45),
                           (13, 'Cours de saut', "Ce cours portera sur la technique de saut d'obstacle pour les débutants", "Collectif", 45),
                           (14, 'Cours de saut', "Ce cours portera sur la technique de saut d'obstacle pour les débutants", "Individuel", 100);


insert into MONITEUR values(1), 
                          (12),
                          (13),
                          (14),
                          (15),
                          (16);


insert into PERSONNE values(1, "Doudeau", "Luis", 2003-10-03, 70, "luis.doudeau@gmail.com", "4 rue des chèvres", 45000, "Orléans", 0607080910, "chèvre123!"), 
                            (2, "Faucher", "Thomas", 2003-07-06, 55, "thelendpvp@icloud.com", "10 chemin du tron", 45000, "Orléans", 0610141820, "TfaucherLMaO@a1"),
                            (3, "De nardi", "Lenny", 2003-11-16, 55, "lenny.denardi@gmail.com", "49 rue de la biche", 45380, "Chaingy", 0708090506, "1!Y!o!Y!o!2"),
                            (4, "Charpentier", "Maxym", 1975-06-01, 99, "Maxlamenace@gmail.com", "45 rue de la menace", 84550, "Mornas", 0710111213, "JvezvoustuarAHAH:"),
                            (5, "Jory", "Jonathan", 2017-05-20, 35,"Jjory@icloud.com", "23 impasse de la groue", 70000, "Vesoul", 0790807010, "JORYGOLEPAS"),
                            (6, "El mechta", "Aymen", 2000-15-12, 100, "mechta@gmail.com", "10 rue d'ivrogne", 40120, "Roquefort", 0615141921, "DO!RM/IR!"),
                            (7, "Plu", "Dinspi", 2002-18-01, 150, "salut@gmail.com", "1 rue du lac", 12000, "Rodez", 0691919191, "INSPI123REV!"),
                            (8, "Plu", "Claude", 1965-01-02, 85, "JCjc@icloud.com", "1 rue du lac", 12000, "Rodez", 0681818181, "JCAHJCAH"),
                            (9, "Chirac", "Jacques", 1989-08-07, 41, "Jesuisunfake@gmail.com", "84 rue du fake", 18260, "Barlieu", 0707080707, "fakercmoi!"),
                            (10, "Retour", "Erve", 2010-10-10, 50, "roides10@icloud.com", "10 rue des dix", 10000, "Troyes", 0710101010, "troyesmais10:p");

insert into PONEYS values(1, "Chacha", 180),
                            (2, "Michella", 30),
                            (3, "Parapluie", 41),
                            (4, "Merveille", 101),
                            (5, "Shakira", 100),
                            (6, "Soulja boy", 55),
                            (7, "Prune", 84),
                            (8, "Virgule", 40),
                            (9, "Bouteille", 62),
                            (10, "Mure", 71);

insert into RESERVER values(2022-09-12 14:30, 1, 1, 1, 01:00:00, true),
                            (2022-09-12 16:30, 2, 14, 2, 02:00:00, false), --pas possible car poidssup inférieur poids
                            (2022-09-13 09:00, 3, 3, 4, 02:00:00, true),
                            (2022-09-13 11:30, 4, 12, 4, 02:00:00, true), -- pas possible car poney doit reposé au moins 1h
                            (2022-09-18 13:45, 5, 9, 7, 02:00:00, false),
                            (2022-09-18 16:45, 6, 11, 7, 01:00:00, true), -- fonctionne si on compte qu'au bout de 1h pile le cheval refonctionne
                            (2022-09-18 17:00, 7, 11, 1, 02:00:00, false),
                            (2022-09-18 18:30, 8, 11, 5, 01:00:00, true), -- CETTE INSERTION + CELLE D'AVANT = 2 SUR LE MEME COURS A LA MM HEURE AVEC CHEVAUX DIFFÉRENTS DONC VOIR SI ON PEUT
                            (2022-09-18 20:20, 9, 2, 3, 01:00:00, false), -- POIDS DU MEC = POIDSSUP CHEVAL DONC NORMALEMENT ÇA FONCTIONNE
                            (2022-09-19 08:00, 2, 14, 1, 02:00:00, false), -- meme mec/cheval que l'insertion 1 sauf qu'il a pas encore payé
                            (2022-09-19 09:30, 2, 10, 1, 01:00:00, true), -- pas possible car insertion d'avant le mec est entrain de faire du cheval deja
