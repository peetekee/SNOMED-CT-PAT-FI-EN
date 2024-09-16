set search_path=snomedct;

drop view if exists snap_fsn;

CREATE VIEW snap_fsn AS
(SELECT distinct d.* FROM 
	snap_description d
    join snap_langrefset rs ON d.id = rs.referencedComponentId
    WHERE d.active = '1' AND d.typeId = '900000000000003001'
    AND rs.active = '1' AND rs.acceptabilityId = '900000000000548007'
    and d.languagecode = 'en'
);