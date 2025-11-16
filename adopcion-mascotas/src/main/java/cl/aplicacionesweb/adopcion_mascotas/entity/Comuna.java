package cl.aplicacionesweb.adopcion_mascotas.entity;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "comuna")
@Data
public class Comuna {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    
    @Column(name = "nombre")
    private String nombre;
}
