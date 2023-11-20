-- Crear la función POSIBLE_RESERVACION
CREATE OR REPLACE FUNCTION POSIBLE_RESERVACION()
RETURNS TRIGGER AS $$
BEGIN
  -- Verificar si existe una disponibilidad para la habitación y fecha dada
  IF EXISTS (
    SELECT 1
    FROM disponibilidad
    WHERE id_habitacion = NEW.id_habitacion
      AND fecha = NEW.fecha_reservada
  ) THEN
    -- Verificar si la habitación está disponible
    IF EXISTS (
      SELECT 1
      FROM disponibilidad
      WHERE id_habitacion = NEW.id_habitacion
        AND fecha = NEW.fecha_reservada
        AND disponible = true
    ) THEN
      -- Actualizar la disponibilidad existente
      UPDATE disponibilidad
      SET disponible = false
      WHERE id_habitacion = NEW.id_habitacion
        AND fecha = NEW.fecha_reservada;
    ELSE
      -- Lanzar un error si la habitación ya está ocupada
      RAISE EXCEPTION 'La habitación ya está ocupada para esa fecha.';
    END IF;
  ELSE
    -- Insertar un nuevo registro en disponibilidad si no existe
    INSERT INTO disponibilidad (id_habitacion, fecha, disponible)
    VALUES (NEW.id_habitacion, NEW.fecha_reservada, false);
  END IF;

  RETURN NEW; -- Continuar con la operación original
EXCEPTION
  WHEN others THEN
    -- Lanzar un error en caso de cualquier excepción
    RAISE EXCEPTION 'Error en la función POSIBLE_RESERVACION: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Crear el trigger verificacion_reservacion
CREATE TRIGGER verificacion_reservacion
BEFORE INSERT ON reservacion
FOR EACH ROW
EXECUTE FUNCTION POSIBLE_RESERVACION();