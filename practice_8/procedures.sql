CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names VARCHAR[], 
    p_phones VARCHAR[],
    OUT p_errors VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    invalid_names VARCHAR[] := '{}';
BEGIN
    FOR i IN 1 .. array_upper(p_names, 1) LOOP
        IF p_phones[i] ~ '^[0-9]{10,}$' THEN
            IF EXISTS (SELECT 1 FROM contacts WHERE name = p_names[i]) THEN
                UPDATE contacts SET phone = p_phones[i] WHERE name = p_names[i];
            ELSE
                INSERT INTO contacts(name, phone) VALUES(p_names[i], p_phones[i]);
            END IF;
        ELSE
            invalid_names := array_append(invalid_names, p_names[i]);
        END IF;
    END LOOP;
    p_errors := invalid_names;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_target VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE name = p_target OR phone = p_target;
END;
$$;