set search_path=snomedct;

drop view if exists snap_synall;

CREATE VIEW snap_synall AS
(SELECT distinct d.* FROM 
	snap_description d
    join snap_langrefset rs ON d.id = rs.referencedComponentId
    WHERE d.active = '1' AND d.typeId = '900000000000013009'
    AND rs.active = '1' AND rs.acceptabilityId IN ('900000000000548007', '900000000000549004')
    and d.languagecode = 'en'
);