set search_path=snomedct;

drop view if exists snap_description;

CREATE VIEW snap_description as (select * from description_f tbl
    where tbl.effectiveTime = (select max(sub.effectiveTime) from description_f sub
                                where sub.id = tbl.id));