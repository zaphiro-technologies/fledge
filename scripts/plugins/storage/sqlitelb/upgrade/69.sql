--- Insert update alerts schedule and process entry

DELETE FROM fledge.scheduled_processes WHERE name = 'update alerts';

INSERT INTO fledge.scheduled_processes ( name, script ) VALUES ( 'update alerts', '["tasks/update_alerts"]' );
INSERT INTO fledge.schedules ( id, schedule_name, process_name, schedule_type,
                                schedule_time, schedule_interval, exclusive, enabled )
       VALUES ( '852cd8e4-3c29-440b-89ca-2c7691b0450d', -- id
                'update alerts',                        -- schedule_name
                'update alerts',                        -- process_name
                2,                                      -- schedule_type (interval)
                '00:05:00',                             -- schedule_time
                '00:00:00',                             -- schedule_interval
                't',                                    -- exclusive
                't'                                     -- enabled
              );


COMMIT;
