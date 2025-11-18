package cl.aplicacionesweb.adopcion_mascotas.controller;

import cl.aplicacionesweb.adopcion_mascotas.dto.AvisoConNotaDTO;
import cl.aplicacionesweb.adopcion_mascotas.service.NotaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;


@Controller
@RequestMapping("/evaluacion")
public class NotaController {
    @Autowired
    private NotaService notaService;
    
    @GetMapping
    public String mostrarEvaluacion(Model model) {
        return "evaluacion";
    }
    
    @GetMapping("/api/avisos")
    @ResponseBody
    public ResponseEntity<List<AvisoConNotaDTO>> listarAvisos() {
        List<AvisoConNotaDTO> avisos = notaService.obtenerAvisosConNota();
        return ResponseEntity.ok(avisos);
    }
    
    @PostMapping("/api/notas")
    @ResponseBody
    public ResponseEntity<?> agregarNota(@RequestBody Map<String, Integer> payload) {
        try {
            Integer avisoId = payload.get("aviso_id");
            Integer nota = payload.get("nota");
            
            if (avisoId == null || nota == null) {
                return ResponseEntity.badRequest().body(
                    Map.of("error", "Parámetros inválidos")
                );
            }
            
            String nuevoPromedio = notaService.agregarNota(avisoId, nota);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("nuevoPromedio", nuevoPromedio);
            
            return ResponseEntity.ok(response);
            
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(
                Map.of("error", e.getMessage())
            );
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body(
                Map.of("error", "Error al agregar nota")
            );
        }
    }
}
