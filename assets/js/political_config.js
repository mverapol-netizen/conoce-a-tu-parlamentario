window.POLITICAL_CONFIG = {
  reviewed: "2026-09-01",
  majority: 78,
  blocks: {
    oposicion: { label: "Oposición", order: 0 },
    no_alineado: { label: "No alineados", order: 1 },
    oficialismo: { label: "Oficialismo", order: 2 }
  },
  parties: {
    "Partido Comunista": { short: "PC", color: "#a9151b", order: 10, alignment: "oposicion" },
    "Frente Amplio": { short: "FA", color: "#4169d8", order: 20, alignment: "oposicion" },
    "Partido Acción Humanista": { short: "AH", color: "#8b4bb4", order: 25, alignment: "oposicion" },
    "Partido Socialista": { short: "PS", color: "#df3b42", order: 30, alignment: "oposicion" },
    "Partido Por la Democracia": { short: "PPD", color: "#e07b35", order: 40, alignment: "oposicion" },
    "Partido Liberal de Chile": { short: "PL", color: "#7047a8", order: 50, alignment: "oposicion" },
    "Partido Radical de Chile": { short: "PR", color: "#87344e", order: 60, alignment: "oposicion" },
    "Partido Demócrata Cristiano": { short: "DC", color: "#27885e", order: 70, alignment: "oposicion" },
    "Federación Regionalista Verde Social": { short: "FRVS", color: "#68a83c", order: 80, alignment: "oposicion" },

    "Partido de la Gente": { short: "PDG", color: "#713c9d", order: 110, alignment: "no_alineado" },
    "Partido Nacional Libertario": { short: "PNL", color: "#262b35", order: 120, alignment: "no_alineado" },

    "Partido Demócratas Chile": { short: "DEM", color: "#e79820", order: 210, alignment: "oficialismo" },
    "Partido Social Cristiano": { short: "PSC", color: "#2b5aa8", order: 220, alignment: "oficialismo" },
    "Partido Cristiano de Chile": { short: "PCh", color: "#2b5aa8", order: 220, alignment: "oficialismo" },
    "Evolución Política": { short: "EVÓPOLI", color: "#22a9c5", order: 230, alignment: "oficialismo" },
    "Renovación Nacional": { short: "RN", color: "#e3323f", order: 240, alignment: "oficialismo" },
    "Unión Demócrata Independiente": { short: "UDI", color: "#efc63b", order: 250, alignment: "oficialismo" },
    "Partido Republicano": { short: "REP", color: "#163d6b", order: 260, alignment: "oficialismo" },

    "Independientes": { short: "IND", color: "#8995a2", order: 130, alignment: "no_alineado" },
    "Independiente": { short: "IND", color: "#8995a2", order: 130, alignment: "no_alineado" },
    "Sin información": { short: "S/I", color: "#aab2bb", order: 140, alignment: "no_alineado" }
  },
  caucusKeywords: [
    ["partido comunista", "Partido Comunista"],
    ["frente amplio", "Frente Amplio"],
    ["accion humanista", "Partido Acción Humanista"],
    ["partido socialista", "Partido Socialista"],
    ["partido por la democracia", "Partido Por la Democracia"],
    ["partido liberal", "Partido Liberal de Chile"],
    ["radical", "Partido Radical de Chile"],
    ["democrata cristiano", "Partido Demócrata Cristiano"],
    ["democracia cristiana", "Partido Demócrata Cristiano"],
    ["regionalista verde", "Federación Regionalista Verde Social"],
    ["partido de la gente", "Partido de la Gente"],
    ["nacional libertario", "Partido Nacional Libertario"],
    ["democratas", "Partido Demócratas Chile"],
    ["social cristiano", "Partido Social Cristiano"],
    ["partido cristiano", "Partido Cristiano de Chile"],
    ["evolucion politica", "Evolución Política"],
    ["renovacion nacional", "Renovación Nacional"],
    ["democrata independiente", "Unión Demócrata Independiente"],
    ["partido republicano", "Partido Republicano"]
  ]
};
