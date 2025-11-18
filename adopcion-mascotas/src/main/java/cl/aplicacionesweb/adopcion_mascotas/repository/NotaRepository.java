package cl.aplicacionesweb.adopcion_mascotas.repository;

import cl.aplicacionesweb.adopcion_mascotas.entity.Nota;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface NotaRepository extends JpaRepository<Nota, Integer> {
    
    @Query("SELECT AVG(n.nota) FROM Nota n WHERE n.avisoId = :avisoId")
    Double calcularPromedioNota(@Param("avisoId") Integer avisoId);
}

