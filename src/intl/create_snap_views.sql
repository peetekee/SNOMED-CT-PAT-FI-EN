-- set the right schema
set
    search_path = snomedct;

-- create snapshot views
drop view if exists snap_langrefset;

create view snap_langrefset as (
    select
        *
    from
        langrefset_f tbl
    where
        tbl.effectiveTime = (
            select
                max(sub.effectiveTime)
            from
                langrefset_f sub
            where
                sub.id = tbl.id
        -- Only include US refset
        ) and tbl.refSetId = '900000000000509007' and tbl.active = '1'
);

-- concept
drop view if exists snap_concept;

create view snap_concept as (
    select
        *
    from
        concept_f tbl
    where
        tbl.effectiveTime = (
            select
                max(sub.effectiveTime)
            from
                concept_f sub
            where
                sub.id = tbl.id
        )
);

-- description
drop view if exists snap_description;

create view snap_description as (
    select
        tbl.*
    from
        description_f tbl join snap_langrefset rs on tbl.id = rs.referencedComponentId
    where
        tbl.effectiveTime = (
            select
                max(sub.effectiveTime)
            from
                description_f sub
            where
                sub.id = tbl.id
        ) and rs.id is not null
);

-- attribute value reference set
drop view if exists snap_attributevaluerefset;

CREATE VIEW snap_attributevaluerefset as (
    select
        *
    from
        attributevaluerefset_f tbl
    where
        tbl.effectiveTime = (
            select
                max(sub.effectiveTime)
            from
                attributevaluerefset_f sub
            where
                sub.id = tbl.id
        )
);

-- association reference set
drop view if exists snap_associationrefset;

CREATE VIEW snap_associationrefset as (
    select
        *
    from
        associationrefset_f tbl
    where
        tbl.effectiveTime = (
            select
                max(sub.effectiveTime)
            from
                associationrefset_f sub
            where
                sub.id = tbl.id
        )
);

-- fully specified name
drop view if exists snap_fsn;

create view snap_fsn as (
    select
        distinct d.*
    from
        snap_description d
        join snap_langrefset rs on d.id = rs.referencedComponentId
    where
        d.active = '1'
        and d.typeId = '900000000000003001'
        and rs.active = '1'
        and rs.acceptabilityId = '900000000000548007'
        and d.languagecode = 'en'
);

-- preferred term
drop view if exists snap_pref;

create view snap_pref as (
    select
        distinct d.*
    from
        snap_description d
        join snap_langrefset rs on d.id = rs.referencedComponentId
    where
        d.active = '1'
        and d.typeId = '900000000000013009'
        and rs.active = '1'
        and rs.acceptabilityId = '900000000000548007'
        and d.languagecode = 'en'
);

-- synonym
drop view if exists snap_syn;

create view snap_syn as (
    select
        distinct d.*
    from
        snap_description d
        join snap_langrefset rs on d.id = rs.referencedComponentId
    where
        d.active = '1'
        and d.typeId = '900000000000013009'
        and rs.active = '1'
        and rs.acceptabilityId = '900000000000549004'
        and d.languagecode = 'en'
);

-- all synonyms
drop view if exists snap_synall;

create view snap_synall as (
    select
        distinct d.*
    from
        snap_description d
        join snap_langrefset rs on d.id = rs.referencedComponentId
    where
        d.active = '1'
        and d.typeId = '900000000000013009'
        and rs.active = '1'
        and rs.acceptabilityId in ('900000000000549004', '900000000000548007')
        and d.languagecode = 'en'
);

create view snap_historical_refset as (
    select
        ar.*
	from
		snap_associationrefset ar
	where
		ar.active = '1' and
		ar.refsetid IN (
    		select
    			r.sourceid
    		from
    			relationship_f r
    		where
    			r.typeid = '116680003' and
    			r.destinationid = '900000000000522004' and
    			r.active = '1'
		)
)
