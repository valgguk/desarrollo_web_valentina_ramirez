
// Invented sample data for the prototype
// id ties rows to detail page
const ADOPCIONES = [
  {
    id: 1,
    publicacion: "A-001",
    fechaPublicacion: "2025-08-18 12:00",
    fechaEntrega: "2025-08-25 12:00",
    region: "Región Metropolitana",
    comuna: "Santiago",
    sector: "Beauchef 850, terraza",
    tipo: "gato",
    cantidad: 1,
    edad: 2,
    unidadEdad: "meses",
    nombreContacto: "María López",
    email: "maria@example.com",
    celular: "+569.12345678",
    contactarPor: [{via:"whatsapp", id:"wa.me/56912345678"}],
    descripcion: "gatito cariñoso encontrado en campus",
    fotos: [
      {"small": "images/item1_photo1_320x240.png", "large": "images/item1_photo1_800x600.png"},
      {"small": "images/item1_photo2_320x240.png", "large": "images/item1_photo2_800x600.png"}
    ]
  },
  {
    id: 2,
    publicacion: "A-002",
    fechaPublicacion: "2025-08-17 09:30",
    fechaEntrega: "2025-08-24 09:30",
    region: "Región Metropolitana",
    comuna: "Providencia",
    sector: "Parque Bustamante",
    tipo: "perro",
    cantidad: 2,
    edad: 1,
    unidadEdad: "años",
    nombreContacto: "Pedro Pérez",
    email: "pedro@example.com",
    celular: "+569.23456789",
    contactarPor: [{via:"instagram", id:"instagram.com/pedro"}],
    descripcion: "perritos hermanos, muy juguetones",
    fotos: [
      {"small": "images/item2_photo1_320x240.png", "large": "images/item2_photo1_800x600.png"},
      {"small": "images/item2_photo2_320x240.png", "large": "images/item2_photo2_800x600.png"}
    ]
  },
  {
    id: 3,
    publicacion: "A-003",
    fechaPublicacion: "2025-08-16 17:45",
    fechaEntrega: "2025-08-17 17:45",
    region: "Región Metropolitana",
    comuna: "Ñuñoa",
    sector: "Plaza Ñuñoa",
    tipo: "gato",
    cantidad: 3,
    edad: 4,
    unidadEdad: "meses",
    nombreContacto: "Valentina R.",
    email: "valentina@example.com",
    celular: "",
    contactarPor: [{via:"telegram", id:"@valentina"}],
    descripcion: "tres gatitos rescatados",
    fotos: [
      {"small": "images/item3_photo1_320x240.png", "large": "images/item3_photo1_800x600.png"},
      {"small": "images/item3_photo2_320x240.png", "large": "images/item3_photo2_800x600.png"}
    ]
  },
  {
    id: 4,
    publicacion: "A-004",
    fechaPublicacion: "2025-08-15 11:15",
    fechaEntrega: "2025-08-20 11:15",
    region: "Región de Valparaíso",
    comuna: "Valparaíso",
    sector: "Cerro Alegre",
    tipo: "perro",
    cantidad: 1,
    edad: 3,
    unidadEdad: "años",
    nombreContacto: "Ana Díaz",
    email: "ana@example.com",
    celular: "+569.87654321",
    contactarPor: [{via:"X", id:"x.com/anad"}],
    descripcion: "perro adulto esterilizado",
    fotos: [
      {"small": "images/item4_photo1_320x240.png", "large": "images/item4_photo1_800x600.png"},
      {"small": "images/item4_photo2_320x240.png", "large": "images/item4_photo2_800x600.png"}
    ]
  },
  {
    id: 5,
    publicacion: "A-005",
    fechaPublicacion: "2025-08-14 16:20",
    fechaEntrega: "2025-08-21 16:20",
    region: "Región de Valparaíso",
    comuna: "Viña del Mar",
    sector: "5 Norte",
    tipo: "gato",
    cantidad: 1,
    edad: 8,
    unidadEdad: "meses",
    nombreContacto: "Luis F.",
    email: "luis@example.com",
    celular: "",
    contactarPor: [{via:"otra", id:"sitio.luis.cl/adopta"}],
    descripcion: "gato muy tranquilo",
    fotos: [
      {"small": "images/item5_photo1_320x240.png", "large": "images/item5_photo1_800x600.png"},
      {"small": "images/item5_photo2_320x240.png", "large": "images/item5_photo2_800x600.png"}
    ]
  }
];
