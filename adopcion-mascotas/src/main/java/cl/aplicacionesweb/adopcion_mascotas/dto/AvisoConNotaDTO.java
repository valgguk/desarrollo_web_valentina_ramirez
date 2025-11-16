package cl.aplicacionesweb.adopcion_mascotas.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AvisoConNotaDTO {
    private Integer id;
    private String fechaPublicacion;
    private String sector;
    private String descripcionMascota; // "1 gato 2 meses"
    private String comuna;
    private String notaPromedio; // "6.5" o "-"
}
