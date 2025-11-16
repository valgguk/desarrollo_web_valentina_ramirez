package cl.aplicacionesweb.adopcion_mascotas.repository;

import cl.aplicacionesweb.adopcion_mascotas.entity.AvisoAdopcion;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AvisoAdopcionRepository extends JpaRepository<AvisoAdopcion, Integer> {
}
