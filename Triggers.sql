drop trigger if exists verifPoids;
drop trigger if exists ajoutPersonneCollectif;
drop trigger if exists ajoutPersonneHoraire;

delimiter |

create trigger verifPoids before insert on RESERVER for each row
    begin 
        declare poidsup decimal(3.3);
        declare poidsPersonne decimal(3.3);
        declare msg VARCHAR(300);
        select poids into poidsPersonne from PERSONNE where idp = new.idp;
        select poidssup into poidsup from PONEYS where idpo = new.idpo;
        if poidsup < poidsPersonne then
            set msg = concat(" Réservation impossible car le poids supporté par le poney d'id : ", new.idpo," est inférieur au poids de la personne d'id : ", new.idp);
            signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
        end if;
    end |


-- trigger permettant que si le cours est un cours collectif, le nombre de personne max est de 10

create trigger ajoutPersonneCollectif before insert on RESERVER for each row
begin
  declare nbmax int;
  declare nbPersonnes int;
  declare typeCours VARCHAR(42);
  declare mes VARCHAR(100);
  set nbmax = 10;
  select IFNULL(count(idp),0) into nbPersonnes from RESERVER where idc = new.idc and jmahms = new.jmahms;
  select typec into typeCours from COURS where idc = new.idc;
  if typeCours = "Collectif" then
    if nbPersonnes + 1 > nbmax then
      set mes = concat ("Inscription impossible à l'activité avec l'id : ", new.idc, " car elle est complète");
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;
  if typeCours = "Individuel" then
    if nbPersonnes <> 0 then
    set mes = concat ("Inscription impossible à l'activité avec l'id : ", new.idc, " car elle est complète");
    signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;
end |


-- permet de vérifier que le client n'a pas déja un cours au horaire de sa nouvelle réservation

delimiter |

create or replace trigger ajoutPersonneHoraire before insert on RESERVER for each row 
begin 
  declare msg VARCHAR(300);
  declare debutAncien time;
  declare dureeAncien time;
  declare debutNew time;
  declare dureeNew time;
  select TIME(jmahms) into debutAncien from RESERVER where idp = new.idp and year(jmahms) = year(new.jmahms) and month(jmahms) = month(new.jmahms) and day(jmahms) = day(new.jmahms);
  select TIME(duree) into dureeAncien from RESERVER where idp = new.idp and year(jmahms) = year(new.jmahms) and month(jmahms) = month(new.jmahms) and day(jmahms) = day(new.jmahms);
  select TIME(new.jmahms) into debutNew from RESERVER where idp = new.idp and year(jmahms) = year(new.jmahms) and month(jmahms) = month(new.jmahms) and day(jmahms) = day(new.jmahms);
  select TIME(new.duree) into dureeNew from RESERVER where idp = new.idp and year(jmahms) = year(new.jmahms) and month(jmahms) = month(new.jmahms) and day(jmahms) = day(new.jmahms);
  if (debutAncien > debutNew and ADDTIME(debutNew, dureeNew) > debutAncien or debutAncien < debutNew and debutNew < ADDTIME(debutAncien, dureeAncien)) then 
    set msg = concat ("Inscription impossible à l'activité car le même client à déja un cours à cette heure");
    signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
  end if;
end |

delimiter ;


delimiter |

create or replace trigger verifHeureRepos before insert on RESERVER for each row
begin
  declare msg VARCHAR(300);
  declare debutAncien time;
  declare dureeAncien time ;
  declare debutNew time;

  select TIME(duree) into dureeAncien from RESERVER where idpo = new.idpo and year(jmahms) = year(new.jmahms) and month(jmahms) = month(new.jmahms) and day(jmahms) = day(new.jmahms) and TIMEDIFF(HOUR(new.jmahms), HOUR(jmahms)) <= TIME("02:00:00");
  if dureeAncien = TIME("02:00:00") then
    set msg = concat ("Inscription impossible à l'activité car le cheval n'a pas eu le temps de se reposer");
    signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
  end if;
end |

delimiter ;
-- trigger sur le repos des chevaux


select TIME(duree) into dureeAncien from RESERVER where idpo = new.idpo and year(jmahms) = year(new.jmahms) 
 and month(jmahms) = month(new.jmahms) and day(jmahms) = day(new.jmahms) and TIMEDIFF(HOUR(new.jmahms), HOUR(jmahms) <= TIME("02:00:00"))