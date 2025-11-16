package cl.aplicacionesweb.adopcion_mascotas.service;

import cl.aplicacionesweb.adopcion_mascotas.dto.AvisoConNotaDTO;
import cl.aplicacionesweb.adopcion_mascotas.entity.AvisoAdopcion;
import cl.aplicacionesweb.adopcion_mascotas.entity.Nota;
import cl.aplicacionesweb.adopcion_mascotas.repository.AvisoAdopcionRepository;
import cl.aplicacionesweb.adopcion_mascotas.repository.NotaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.lang.NonNull;

import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

@Service
public class NotaService {
    
    @Autowired
    private NotaRepository notaRepository;
    
    @Autowired
    private AvisoAdopcionRepository avisoRepository;
    
    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd");
    
    public List<AvisoConNotaDTO> obtenerAvisosConNota() {
        List<AvisoAdopcion> avisos = avisoRepository.findAll();
        
        return avisos.stream().map(aviso -> {
            String fechaStr = aviso.getFechaIngreso() != null 
                ? aviso.getFechaIngreso().format(DATE_FORMATTER) 
                : "-";
            
            String descripcion = String.format("%d %s %d %s", 
                aviso.getCantidad(),
                aviso.getTipo(),
                aviso.getEdad(),
                "m".equals(aviso.getUnidadMedida()) ? "meses" : "años"
            );
            
            String comunaNombre = aviso.getComuna() != null 
                ? aviso.getComuna().getNombre() 
                : "-";
            
            Double promedio = notaRepository.calcularPromedioNota(aviso.getId());
            String notaStr = promedio != null 
                ? String.format("%.1f", promedio) 
                : "-";
            
            return new AvisoConNotaDTO(
                aviso.getId(),
                fechaStr,
                aviso.getSector() != null ? aviso.getSector() : "-",
                descripcion,
                comunaNombre,
                notaStr
            );
        }).collect(Collectors.toList());
    }
    
    @Transactional
    public String agregarNota(@NonNull Integer avisoId, @NonNull Integer valorNota) {
        // Validar rango
        if (valorNota < 1 || valorNota > 7) {
            throw new IllegalArgumentException("La nota debe estar entre 1 y 7");
        }
        
        // Verificar que el aviso existe
        if (!avisoRepository.existsById(avisoId)) {
            throw new IllegalArgumentException("Aviso no encontrado");
        }
        
        // Crear y guardar nota
        Nota nota = new Nota();
        nota.setAvisoId(avisoId);
        nota.setNota(valorNota);
        notaRepository.save(nota);
        
        // Calcular nuevo promedio
        Double promedio = notaRepository.calcularPromedioNota(avisoId);
        return promedio != null ? String.format("%.1f", promedio) : "-";
    }
}
