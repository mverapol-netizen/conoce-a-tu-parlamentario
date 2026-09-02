window.POLITICAL_CONFIG = {
  reviewed: "2026-09-02",
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

    "Ind. Comité PC": { short: "IND·PC", color: "#a9151b", order: 12, alignment: "oposicion" },
    "Ind. Comité FA": { short: "IND·FA", color: "#4169d8", order: 22, alignment: "oposicion" },
    "Ind. Comité PS–PL–PR": { short: "IND·PS/PL/PR", color: "#b74a63", order: 35, alignment: "oposicion" },
    "Ind. Comité PPD": { short: "IND·PPD", color: "#e07b35", order: 42, alignment: "oposicion" },
    "Ind. Comité DC–FRVS": { short: "IND·DC/FRVS", color: "#4d9457", order: 75, alignment: "oposicion" },

    "Partido de la Gente": { short: "PDG", color: "#713c9d", order: 110, alignment: "no_alineado" },
    "Partido Nacional Libertario": { short: "PNL", color: "#262b35", order: 120, alignment: "no_alineado" },
    "Ind. Comité PDG": { short: "IND·PDG", color: "#713c9d", order: 112, alignment: "no_alineado" },
    "Ind. Comité PNL": { short: "IND·PNL", color: "#262b35", order: 122, alignment: "no_alineado" },
    "Independientes": { short: "IND", color: "#8995a2", order: 130, alignment: "no_alineado" },
    "Independiente": { short: "IND", color: "#8995a2", order: 130, alignment: "no_alineado" },
    "Ind. sin bancada definida": { short: "IND", color: "#8995a2", order: 135, alignment: "no_alineado" },

    "Partido Demócratas Chile": { short: "DEM", color: "#e79820", order: 210, alignment: "oficialismo" },
    "Partido Social Cristiano": { short: "PSC", color: "#2b5aa8", order: 220, alignment: "oficialismo" },
    "Partido Cristiano de Chile": { short: "PCh", color: "#2b5aa8", order: 220, alignment: "oficialismo" },
    "Evolución Política": { short: "EVÓPOLI", color: "#22a9c5", order: 230, alignment: "oficialismo" },
    "Renovación Nacional": { short: "RN", color: "#e3323f", order: 240, alignment: "oficialismo" },
    "Unión Demócrata Independiente": { short: "UDI", color: "#efc63b", order: 250, alignment: "oficialismo" },
    "Partido Republicano": { short: "REP", color: "#163d6b", order: 260, alignment: "oficialismo" },
    "Ind. Comité RN–Evópoli": { short: "IND·RN/EVOP", color: "#d65362", order: 242, alignment: "oficialismo" },
    "Ind. Comité UDI": { short: "IND·UDI", color: "#efc63b", order: 252, alignment: "oficialismo" },
    "Ind. Comité Republicano": { short: "IND·REP", color: "#163d6b", order: 262, alignment: "oficialismo" },

    "Sin información": { short: "S/I", color: "#aab2bb", order: 999, alignment: "no_alineado" }
  },
  caucusKeywords: [
    ["comite comunista", "Ind. Comité PC"],
    ["frente amplio", "Ind. Comité FA"],
    ["socialista liberal radical", "Ind. Comité PS–PL–PR"],
    ["partido por la democracia", "Ind. Comité PPD"],
    ["democracia cristiana", "Ind. Comité DC–FRVS"],
    ["regionalista verde", "Ind. Comité DC–FRVS"],
    ["partido de la gente", "Ind. Comité PDG"],
    ["nacional libertario", "Ind. Comité PNL"],
    ["renovacion nacional", "Ind. Comité RN–Evópoli"],
    ["democrata independiente", "Ind. Comité UDI"],
    ["partido republicano", "Ind. Comité Republicano"],
    ["por definir", "Ind. sin bancada definida"]
  ]
};
