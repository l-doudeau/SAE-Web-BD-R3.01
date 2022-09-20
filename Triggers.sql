delimiter |

create or replace trigger verifPoids before insert on RESERVER for each row
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
