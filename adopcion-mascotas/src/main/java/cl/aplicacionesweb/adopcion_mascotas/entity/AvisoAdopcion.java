package cl.aplicacionesweb.adopcion_mascotas.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "aviso_adopcion")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class AvisoAdopcion {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    
    @Column(name = "fecha_ingreso")
    private LocalDateTime fechaIngreso;
    
    @Column(name = "sector")
    private String sector;
    
    @Column(name = "tipo")
    private String tipo;
    
    @Column(name = "cantidad")
    private Integer cantidad;
    
    @Column(name = "edad")
    private Integer edad;
    
    @Column(name = "unidad_medida")
    private String unidadMedida;
    
    @Column(name = "comuna_id")
    private Integer comunaId;
    
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "comuna_id", insertable = false, updatable = false)
    private Comuna comuna;
    
    @OneToMany(mappedBy = "aviso", fetch = FetchType.LAZY)
    private List<Nota> notas;
}
