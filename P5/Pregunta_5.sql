CREATE PROCEDURE Difenciar_Dos_Cadenas
    @cadena1 varchar(20),
    @cadena2 varchar(20)
AS
BEGIN
    DECLARE @longitud_cadena1 int,
            @longitud_cadena2 int,
            @contador int,
            @caracter varchar(4),
            @sql nvarchar(4000),
            @columna varchar(10),
            @longitud int

    SET @sql = 'CREATE TABLE nombre (';

    SET @longitud_cadena1 = LEN(@cadena1)
    SET @longitud_cadena2 = LEN(@cadena2)
    SET @contador = 0

    WHILE @contador < @longitud_cadena1
    BEGIN
        SET @caracter = LEFT(@cadena1, 1) + CAST(@contador as varchar(1))
        SET @cadena1 = RIGHT(@cadena1, LEN(@cadena1) - 1)
        SET @sql = @sql + @caracter + ' int,'
        SET @contador = @contador + 1
    END

    SET @sql = LEFT(@sql, LEN(@sql) - 1)
    SET @sql = @sql + ')'
    PRINT(@sql)
    EXEC sp_executesql @sql


    SET @contador = 0
    WHILE @contador < @longitud_cadena2
    BEGIN
        SET @caracter = LEFT(@cadena2, 1)
        SET @cadena2 = RIGHT(@cadena2, LEN(@cadena2) - 1)

        SELECT TOP 1 @columna = COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME='nombre' AND LEFT(COLUMN_NAME, 1) = @caracter AND ORDINAL_POSITION >= @contador

        SET @sql='INSERT INTO nombre ('+@columna+') VALUES (1)'
        EXEC sp_executesql @sql
        SET @contador = @contador + 1
    END

    SET @contador = 1

    SELECT @longitud = COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'nombre'

    SET @sql = ''

    WHILE @contador <= @longitud
    BEGIN
        SELECT @columna = COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'nombre' AND ORDINAL_POSITION = @contador
        SET @sql = @sql + 'SUM(' + @columna + '),'
        SET @contador = @contador + 1
    END

    SET @sql = 'SELECT '+ LEFT(@sql, LEN(@sql) - 1)
    SET @sql = @sql + ' FROM nombre'
    PRINT (@sql)

    EXEC sp_executesql @sql

    SELECT * 
    FROM nombre
END

DROP TABLE nombre
EXEC Difenciar_Dos_Cadenas 'ZULEMA', 'ZULMA';
