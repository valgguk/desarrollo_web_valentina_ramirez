package cl.aplicacionesweb.adopcion_mascotas.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Entity
@Table(name = "nota")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Nota {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    
    @Column(name = "aviso_id", nullable = false)
    private Integer avisoId;
    
    @Column(name = "nota", nullable = false)
    private Integer nota;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "aviso_id", insertable = false, updatable = false)
    private AvisoAdopcion aviso;
}
