drop trigger if exists verifPoids;

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

delimiter ;

-- si le cours est un cours collectif, le nombre de personne max est 10

delimiter |

create or replace trigger ajoutPersonneCollectif before insert on RESERVER for each row
begin
  declare nbmax int;
  declare nbPersonnes int;
  declare typeCours VARCHAR(42);
  declare mes VARCHAR(100);
  set nbmax = 10;
  select count(idp) into nbPersonnes from RESERVER where idc = new.idc and jmahms = new.jmahms;
  select typec into typeCours from RESERVER where idc = new.idc and jmahms = new.jmahms;
  if typeCours = "Collectif" then
    if nbPersonnes + 1 > nbmax then
      set mes = concat ("Inscription impossible à l'activité avec l'id : ", new.ida, " car elle est complète");
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    enf if;
  end if;
end |
delimiter ;