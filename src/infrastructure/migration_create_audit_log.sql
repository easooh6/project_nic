CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    actor_user_id BIGINT REFERENCES "user"(id),
    action TEXT NOT NULL,
    entity TEXT NOT NULL,
    entity_id BIGINT NULL,
    meta JSONB DEFAULT '{}'::jsonb,
    ts TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_log_entity ON audit_log (entity, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_actor ON audit_log (actor_user_id, ts);
CREATE INDEX IF NOT EXISTS idx_audit_log_ts ON audit_log (ts DESC);
