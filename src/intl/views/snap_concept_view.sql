set search_path=snomedct;

drop view if exists snap_concept;

CREATE VIEW snap_concept as (select * from concept_f tbl
    where tbl.effectiveTime = (select max(sub.effectiveTime) from concept_f sub
                                where sub.id = tbl.id));