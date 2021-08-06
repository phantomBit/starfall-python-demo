CREATE TABLE IF NOT EXISTS `widgets`
(
    `id`        INTEGER PRIMARY KEY AUTOINCREMENT,
    `name`      VARCHAR(64) NOT NULL,
    `number`    INTEGER,
    `createdOn` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    `updatedOn` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TRIGGER widgets_on_update
    AFTER UPDATE OF `id`, `name`, `number`
    ON `widgets`

    FOR EACH ROW
BEGIN
    UPDATE `widgets`
    SET updatedOn = DATETIME('NOW')
    WHERE rowid = new.rowid;
END;
