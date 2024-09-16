set search_path=snomedct;

drop view if exists snap_langrefset;

CREATE VIEW snap_langrefset as (select * from langrefset_f tbl
    where tbl.effectiveTime = (select max(sub.effectiveTime) from langrefset_f sub
                                where sub.id = tbl.id));