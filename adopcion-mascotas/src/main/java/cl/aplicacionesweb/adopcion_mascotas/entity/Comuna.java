package cl.aplicacionesweb.adopcion_mascotas.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Entity
@Table(name = "comuna")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Comuna {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    
    @Column(name = "nombre")
    private String nombre;
}
