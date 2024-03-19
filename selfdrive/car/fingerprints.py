from openpilot.selfdrive.car.interfaces import get_interface_attr
from openpilot.selfdrive.car.body.values import CAR as BODY
from openpilot.selfdrive.car.chrysler.values import CAR as CHRYSLER
from openpilot.selfdrive.car.ford.values import CAR as FORD
from openpilot.selfdrive.car.gm.values import CAR as GM
from openpilot.selfdrive.car.honda.values import CAR as HONDA
from openpilot.selfdrive.car.hyundai.values import CAR as HYUNDAI
from openpilot.selfdrive.car.mazda.values import CAR as MAZDA
from openpilot.selfdrive.car.nissan.values import CAR as NISSAN
from openpilot.selfdrive.car.subaru.values import CAR as SUBARU
from openpilot.selfdrive.car.tesla.values import CAR as TESLA
from openpilot.selfdrive.car.toyota.values import CAR as TOYOTA
from openpilot.selfdrive.car.volkswagen.values import CAR as VW

FW_VERSIONS = get_interface_attr('FW_VERSIONS', combine_brands=True, ignore_none=True)
_FINGERPRINTS = get_interface_attr('FINGERPRINTS', combine_brands=True, ignore_none=True)

_DEBUG_ADDRESS = {1880: 8}   # reserved for debug purposes


def is_valid_for_fingerprint(msg, car_fingerprint: dict[int, int]):
  adr = msg.address
  # ignore addresses that are more than 11 bits
  return (adr in car_fingerprint and car_fingerprint[adr] == len(msg.dat)) or adr >= 0x800


def eliminate_incompatible_cars(msg, candidate_cars):
  """Removes cars that could not have sent msg.

     Inputs:
      msg: A cereal/log CanData message from the car.
      candidate_cars: A list of cars to consider.

     Returns:
      A list containing the subset of candidate_cars that could have sent msg.
  """
  compatible_cars = []

  for car_name in candidate_cars:
    car_fingerprints = _FINGERPRINTS[car_name]

    for fingerprint in car_fingerprints:
      # add alien debug address
      if is_valid_for_fingerprint(msg, fingerprint | _DEBUG_ADDRESS):
        compatible_cars.append(car_name)
        break

  return compatible_cars


def all_known_cars():
  """Returns a list of all known car strings."""
  return list({*FW_VERSIONS.keys(), *_FINGERPRINTS.keys()})


def all_legacy_fingerprint_cars():
  """Returns a list of all known car strings, FPv1 only."""
  return list(_FINGERPRINTS.keys())


# A dict that maps old platform strings to their latest representations
MIGRATION = {
  "ACURA ILX 2016 ACURAWATCH PLUS": HONDA.ACURA_ILX,
  "ACURA RDX 2018 ACURAWATCH PLUS": HONDA.ACURA_RDX,
  "ACURA RDX 2020 TECH": HONDA.ACURA_RDX_3G,
  "AUDI A3": VW.AUDI_A3_MK3,
  "HONDA ACCORD 2018 HYBRID TOURING": HONDA.ACCORD,
  "HONDA ACCORD 1.5T 2018": HONDA.ACCORD,
  "HONDA ACCORD 2018 LX 1.5T": HONDA.ACCORD,
  "HONDA ACCORD 2018 SPORT 2T": HONDA.ACCORD,
  "HONDA ACCORD 2T 2018": HONDA.ACCORD,
  "HONDA ACCORD HYBRID 2018": HONDA.ACCORD,
  "HONDA CIVIC 2016 TOURING": HONDA.CIVIC,
  "HONDA CIVIC HATCHBACK 2017 SEDAN/COUPE 2019": HONDA.CIVIC_BOSCH,
  "HONDA CIVIC SEDAN 1.6 DIESEL": HONDA.CIVIC_BOSCH_DIESEL,
  "HONDA CR-V 2016 EXECUTIVE": HONDA.CRV_EU,
  "HONDA CR-V 2016 TOURING": HONDA.CRV,
  "HONDA CR-V 2017 EX": HONDA.CRV_5G,
  "HONDA CR-V 2019 HYBRID": HONDA.CRV_HYBRID,
  "HONDA FIT 2018 EX": HONDA.FIT,
  "HONDA HRV 2019 TOURING": HONDA.HRV,
  "HONDA INSIGHT 2019 TOURING": HONDA.INSIGHT,
  "HONDA ODYSSEY 2018 EX-L": HONDA.ODYSSEY,
  "HONDA ODYSSEY 2019 EXCLUSIVE CHN": HONDA.ODYSSEY_CHN,
  "HONDA PILOT 2017 TOURING": HONDA.PILOT,
  "HONDA PILOT 2019 ELITE": HONDA.PILOT,
  "HONDA PILOT 2019": HONDA.PILOT,
  "HONDA PASSPORT 2021": HONDA.PILOT,
  "HONDA RIDGELINE 2017 BLACK EDITION": HONDA.RIDGELINE,
  "LEXUS CT 200H 2018": TOYOTA.LEXUS_CTH,
  "LEXUS ES 300H 2018": TOYOTA.LEXUS_ES,
  "LEXUS ES 300H 2019": TOYOTA.LEXUS_ES_TSS2,
  "LEXUS IS300 2018": TOYOTA.LEXUS_IS,
  "LEXUS NX300 2018": TOYOTA.LEXUS_NX,
  "LEXUS NX300H 2018": TOYOTA.LEXUS_NX,
  "LEXUS RX 350 2016": TOYOTA.LEXUS_RX,
  "LEXUS RX350 2020": TOYOTA.LEXUS_RX_TSS2,
  "LEXUS RX450 HYBRID 2020": TOYOTA.LEXUS_RX_TSS2,
  "TOYOTA SIENNA XLE 2018": TOYOTA.SIENNA,
  "TOYOTA C-HR HYBRID 2018": TOYOTA.CHR,
  "TOYOTA COROLLA HYBRID TSS2 2019": TOYOTA.COROLLA_TSS2,
  "TOYOTA RAV4 HYBRID 2019": TOYOTA.RAV4_TSS2,
  "LEXUS ES HYBRID 2019": TOYOTA.LEXUS_ES_TSS2,
  "LEXUS NX HYBRID 2018": TOYOTA.LEXUS_NX,
  "LEXUS NX HYBRID 2020": TOYOTA.LEXUS_NX_TSS2,
  "LEXUS RX HYBRID 2020": TOYOTA.LEXUS_RX_TSS2,
  "TOYOTA ALPHARD HYBRID 2021": TOYOTA.ALPHARD_TSS2,
  "TOYOTA AVALON HYBRID 2019": TOYOTA.AVALON_2019,
  "TOYOTA AVALON HYBRID 2022": TOYOTA.AVALON_TSS2,
  "TOYOTA CAMRY HYBRID 2018": TOYOTA.CAMRY,
  "TOYOTA CAMRY HYBRID 2021": TOYOTA.CAMRY_TSS2,
  "TOYOTA C-HR HYBRID 2022": TOYOTA.CHR_TSS2,
  "TOYOTA HIGHLANDER HYBRID 2020": TOYOTA.HIGHLANDER_TSS2,
  "TOYOTA RAV4 HYBRID 2022": TOYOTA.RAV4_TSS2_2022,
  "TOYOTA RAV4 HYBRID 2023": TOYOTA.RAV4_TSS2_2023,
  "TOYOTA HIGHLANDER HYBRID 2018": TOYOTA.HIGHLANDER,
  "LEXUS ES HYBRID 2018": TOYOTA.LEXUS_ES,
  "LEXUS RX HYBRID 2017": TOYOTA.LEXUS_RX,
  #"HYUNDAI ELANTRA LIMITED ULTIMATE 2017": HYUNDAI.ELANTRA,
  #"HYUNDAI SANTA FE LIMITED 2019": HYUNDAI.SANTA_FE,
  #"HYUNDAI TUCSON DIESEL 2019": HYUNDAI.TUCSON,
  #"HYUNDAI TUCSON HYBRID 4TH GEN": HYUNDAI.TUCSON_4TH_GEN,
  #"KIA SPORTAGE HYBRID 5TH GEN": HYUNDAI.KIA_SPORTAGE_5TH_GEN,
  #"KIA SORENTO PLUG-IN HYBRID 4TH GEN": HYUNDAI.KIA_SORENTO_HEV_4TH_GEN,
  #"KIA OPTIMA 2016": HYUNDAI.KIA_OPTIMA_G4,
  #"KIA OPTIMA 2019": HYUNDAI.KIA_OPTIMA_G4_FL,
  #"KIA OPTIMA SX 2019 & 2016": HYUNDAI.KIA_OPTIMA_G4_FL,

  # Removal of platform_str, see https://github.com/commaai/openpilot/pull/31868/
  "COMMA BODY": BODY.BODY,
  "CHRYSLER PACIFICA HYBRID 2017": CHRYSLER.PACIFICA_2017_HYBRID,
  "CHRYSLER PACIFICA HYBRID 2018": CHRYSLER.PACIFICA_2018_HYBRID,
  "CHRYSLER PACIFICA HYBRID 2019": CHRYSLER.PACIFICA_2019_HYBRID,
  "CHRYSLER PACIFICA 2018": CHRYSLER.PACIFICA_2018,
  "CHRYSLER PACIFICA 2020": CHRYSLER.PACIFICA_2020,
  "DODGE DURANGO 2021": CHRYSLER.DODGE_DURANGO,
  "RAM 1500 5TH GEN": CHRYSLER.RAM_1500_5TH_GEN,
  "RAM HD 5TH GEN": CHRYSLER.RAM_HD_5TH_GEN,
  "FORD BRONCO SPORT 1ST GEN": FORD.BRONCO_SPORT_MK1,
  "FORD ESCAPE 4TH GEN": FORD.ESCAPE_MK4,
  "FORD EXPLORER 6TH GEN": FORD.EXPLORER_MK6,
  "FORD F-150 14TH GEN": FORD.F_150_MK14,
  "FORD F-150 LIGHTNING 1ST GEN": FORD.F_150_LIGHTNING_MK1,
  "FORD FOCUS 4TH GEN": FORD.FOCUS_MK4,
  "FORD MAVERICK 1ST GEN": FORD.MAVERICK_MK1,
  "FORD MUSTANG MACH-E 1ST GEN": FORD.MUSTANG_MACH_E_MK1,
  "HOLDEN ASTRA RS-V BK 2017": GM.HOLDEN_ASTRA,
  "CHEVROLET VOLT PREMIER 2017": GM.VOLT,
  "CADILLAC ATS Premium Performance 2018": GM.CADILLAC_ATS,
  "CHEVROLET MALIBU PREMIER 2017": GM.MALIBU,
  "GMC ACADIA DENALI 2018": GM.ACADIA,
  "BUICK LACROSSE 2017": GM.BUICK_LACROSSE,
  "BUICK REGAL ESSENCE 2018": GM.BUICK_REGAL,
  "CADILLAC ESCALADE 2017": GM.ESCALADE,
  "CADILLAC ESCALADE ESV 2016": GM.ESCALADE_ESV,
  "CADILLAC ESCALADE ESV 2019": GM.ESCALADE_ESV_2019,
  "CHEVROLET BOLT EUV 2022": GM.BOLT_EUV,
  "CHEVROLET SILVERADO 1500 2020": GM.SILVERADO,
  "CHEVROLET EQUINOX 2019": GM.EQUINOX,
  "CHEVROLET TRAILBLAZER 2021": GM.TRAILBLAZER,
  "HONDA ACCORD 2018": HONDA.ACCORD,
  "HONDA CIVIC (BOSCH) 2019": HONDA.CIVIC_BOSCH,
  "HONDA CIVIC SEDAN 1.6 DIESEL 2019": HONDA.CIVIC_BOSCH_DIESEL,
  "HONDA CIVIC 2022": HONDA.CIVIC_2022,
  "HONDA CR-V 2017": HONDA.CRV_5G,
  "HONDA CR-V HYBRID 2019": HONDA.CRV_HYBRID,
  "HONDA HR-V 2023": HONDA.HRV_3G,
  "ACURA RDX 2020": HONDA.ACURA_RDX_3G,
  "HONDA INSIGHT 2019": HONDA.INSIGHT,
  "HONDA E 2020": HONDA.HONDA_E,
  "ACURA ILX 2016": HONDA.ACURA_ILX,
  "HONDA CR-V 2016": HONDA.CRV,
  "HONDA CR-V EU 2016": HONDA.CRV_EU,
  "HONDA FIT 2018": HONDA.FIT,
  "HONDA FREED 2020": HONDA.FREED,
  "HONDA HRV 2019": HONDA.HRV,
  "HONDA ODYSSEY 2018": HONDA.ODYSSEY,
  "HONDA ODYSSEY CHN 2019": HONDA.ODYSSEY_CHN,
  "ACURA RDX 2018": HONDA.ACURA_RDX,
  "HONDA PILOT 2017": HONDA.PILOT,
  "HONDA RIDGELINE 2017": HONDA.RIDGELINE,
  "HONDA CIVIC 2016": HONDA.CIVIC,
  "HYUNDAI AZERA 6TH GEN": HYUNDAI.AZERA_6TH_GEN,
  "HYUNDAI AZERA HYBRID 6TH GEN": HYUNDAI.AZERA_HEV_6TH_GEN,
  "HYUNDAI ELANTRA 2017": HYUNDAI.ELANTRA,
  "HYUNDAI I30 N LINE 2019 & GT 2018 DCT": HYUNDAI.ELANTRA_GT_I30,
  "HYUNDAI ELANTRA 2021": HYUNDAI.ELANTRA_2021,
  "HYUNDAI ELANTRA HYBRID 2021": HYUNDAI.ELANTRA_HEV_2021,
  "HYUNDAI GENESIS 2015-2016": HYUNDAI.HYUNDAI_GENESIS,
  "HYUNDAI IONIQ HYBRID 2017-2019": HYUNDAI.IONIQ,
  "HYUNDAI IONIQ HYBRID 2020-2022": HYUNDAI.IONIQ_HEV_2022,
  "HYUNDAI IONIQ ELECTRIC LIMITED 2019": HYUNDAI.IONIQ_EV_LTD,
  "HYUNDAI IONIQ ELECTRIC 2020": HYUNDAI.IONIQ_EV_2020,
  "HYUNDAI IONIQ PLUG-IN HYBRID 2019": HYUNDAI.IONIQ_PHEV_2019,
  "HYUNDAI IONIQ PHEV 2020": HYUNDAI.IONIQ_PHEV,
  "HYUNDAI KONA 2020": HYUNDAI.KONA,
  "HYUNDAI KONA ELECTRIC 2019": HYUNDAI.KONA_EV,
  "HYUNDAI KONA ELECTRIC 2022": HYUNDAI.KONA_EV_2022,
  "HYUNDAI KONA ELECTRIC 2ND GEN": HYUNDAI.KONA_EV_2ND_GEN,
  "HYUNDAI KONA HYBRID 2020": HYUNDAI.KONA_HEV,
  "HYUNDAI SANTA FE 2019": HYUNDAI.SANTA_FE,
  "HYUNDAI SANTA FE 2022": HYUNDAI.SANTA_FE_2022,
  "HYUNDAI SANTA FE HYBRID 2022": HYUNDAI.SANTA_FE_HEV_2022,
  "HYUNDAI SANTA FE PlUG-IN HYBRID 2022": HYUNDAI.SANTA_FE_PHEV_2022,
  "HYUNDAI SONATA 2020": HYUNDAI.SONATA,
  "HYUNDAI SONATA 2019": HYUNDAI.SONATA_LF,
  "HYUNDAI STARIA 4TH GEN": HYUNDAI.STARIA_4TH_GEN,
  "HYUNDAI TUCSON 2019": HYUNDAI.TUCSON,
  "HYUNDAI PALISADE 2020": HYUNDAI.PALISADE,
  "HYUNDAI VELOSTER 2019": HYUNDAI.VELOSTER,
  "HYUNDAI SONATA HYBRID 2021": HYUNDAI.SONATA_HYBRID,
  "HYUNDAI IONIQ 5 2022": HYUNDAI.IONIQ_5,
  "HYUNDAI IONIQ 6 2023": HYUNDAI.IONIQ_6,
  "HYUNDAI TUCSON 4TH GEN": HYUNDAI.TUCSON_4TH_GEN,
  "HYUNDAI SANTA CRUZ 1ST GEN": HYUNDAI.SANTA_CRUZ_1ST_GEN,
  "HYUNDAI CUSTIN 1ST GEN": HYUNDAI.CUSTIN_1ST_GEN,
  "KIA FORTE E 2018 & GT 2021": HYUNDAI.KIA_FORTE,
  "KIA K5 2021": HYUNDAI.KIA_K5_2021,
  "KIA K5 HYBRID 2020": HYUNDAI.KIA_K5_HEV_2020,
  "KIA K8 HYBRID 1ST GEN": HYUNDAI.KIA_K8_HEV_1ST_GEN,
  "KIA NIRO EV 2020": HYUNDAI.KIA_NIRO_EV,
  "KIA NIRO EV 2ND GEN": HYUNDAI.KIA_NIRO_EV_2ND_GEN,
  "KIA NIRO HYBRID 2019": HYUNDAI.KIA_NIRO_PHEV,
  "KIA NIRO PLUG-IN HYBRID 2022": HYUNDAI.KIA_NIRO_PHEV_2022,
  "KIA NIRO HYBRID 2021": HYUNDAI.KIA_NIRO_HEV_2021,
  "KIA NIRO HYBRID 2ND GEN": HYUNDAI.KIA_NIRO_HEV_2ND_GEN,
  "KIA OPTIMA 4TH GEN": HYUNDAI.KIA_OPTIMA_G4,
  "KIA OPTIMA 4TH GEN FACELIFT": HYUNDAI.KIA_OPTIMA_G4_FL,
  "KIA OPTIMA HYBRID 2017 & SPORTS 2019": HYUNDAI.KIA_OPTIMA_H,
  "KIA OPTIMA HYBRID 4TH GEN FACELIFT": HYUNDAI.KIA_OPTIMA_H_G4_FL,
  "KIA SELTOS 2021": HYUNDAI.KIA_SELTOS,
  "KIA SPORTAGE 5TH GEN": HYUNDAI.KIA_SPORTAGE_5TH_GEN,
  "KIA SORENTO GT LINE 2018": HYUNDAI.KIA_SORENTO,
  "KIA SORENTO 4TH GEN": HYUNDAI.KIA_SORENTO_4TH_GEN,
  "KIA SORENTO HYBRID 4TH GEN": HYUNDAI.KIA_SORENTO_HEV_4TH_GEN,
  "KIA STINGER GT2 2018": HYUNDAI.KIA_STINGER,
  "KIA STINGER 2022": HYUNDAI.KIA_STINGER_2022,
  "KIA CEED INTRO ED 2019": HYUNDAI.KIA_CEED,
  "KIA EV6 2022": HYUNDAI.KIA_EV6,
  "KIA CARNIVAL 4TH GEN": HYUNDAI.KIA_CARNIVAL_4TH_GEN,
  "GENESIS GV60 ELECTRIC 1ST GEN": HYUNDAI.GENESIS_GV60_EV_1ST_GEN,
  "GENESIS G70 2018": HYUNDAI.GENESIS_G70,
  "GENESIS G70 2020": HYUNDAI.GENESIS_G70_2020,
  "GENESIS GV70 1ST GEN": HYUNDAI.GENESIS_GV70_1ST_GEN,
  "GENESIS G80 2017": HYUNDAI.GENESIS_G80,
  "GENESIS G90 2017": HYUNDAI.GENESIS_G90,
  "GENESIS GV80 2023": HYUNDAI.GENESIS_GV80,
  "MAZDA CX-5": MAZDA.CX5,
  "MAZDA CX-9": MAZDA.CX9,
  "MAZDA 3": MAZDA.MAZDA3,
  "MAZDA 6": MAZDA.MAZDA6,
  "MAZDA CX-9 2021": MAZDA.CX9_2021,
  "MAZDA CX-5 2022": MAZDA.CX5_2022,
  "NISSAN X-TRAIL 2017": NISSAN.XTRAIL,
  "NISSAN LEAF 2018": NISSAN.LEAF,
  "NISSAN ROGUE 2019": NISSAN.ROGUE,
  "NISSAN ALTIMA 2020": NISSAN.ALTIMA,
  "SUBARU ASCENT LIMITED 2019": SUBARU.ASCENT,
  "SUBARU OUTBACK 6TH GEN": SUBARU.OUTBACK,
  "SUBARU LEGACY 7TH GEN": SUBARU.LEGACY,
  "SUBARU IMPREZA LIMITED 2019": SUBARU.IMPREZA,
  "SUBARU IMPREZA SPORT 2020": SUBARU.IMPREZA_2020,
  "SUBARU CROSSTREK HYBRID 2020": SUBARU.CROSSTREK_HYBRID,
  "SUBARU FORESTER 2019": SUBARU.FORESTER,
  "SUBARU FORESTER HYBRID 2020": SUBARU.FORESTER_HYBRID,
  "SUBARU FORESTER 2017 - 2018": SUBARU.FORESTER_PREGLOBAL,
  "SUBARU LEGACY 2015 - 2018": SUBARU.LEGACY_PREGLOBAL,
  "SUBARU OUTBACK 2015 - 2017": SUBARU.OUTBACK_PREGLOBAL,
  "SUBARU OUTBACK 2018 - 2019": SUBARU.OUTBACK_PREGLOBAL_2018,
  "SUBARU FORESTER 2022": SUBARU.FORESTER_2022,
  "SUBARU OUTBACK 7TH GEN": SUBARU.OUTBACK_2023,
  "SUBARU ASCENT 2023": SUBARU.ASCENT_2023,
  'TESLA AP1 MODEL S': TESLA.AP1_MODELS,
  'TESLA AP2 MODEL S': TESLA.AP2_MODELS,
  'TESLA MODEL S RAVEN': TESLA.MODELS_RAVEN,
  "TOYOTA ALPHARD 2020": TOYOTA.ALPHARD_TSS2,
  "TOYOTA AVALON 2016": TOYOTA.AVALON,
  "TOYOTA AVALON 2019": TOYOTA.AVALON_2019,
  "TOYOTA AVALON 2022": TOYOTA.AVALON_TSS2,
  "TOYOTA CAMRY 2018": TOYOTA.CAMRY,
  "TOYOTA CAMRY 2021": TOYOTA.CAMRY_TSS2,
  "TOYOTA C-HR 2018": TOYOTA.CHR,
  "TOYOTA C-HR 2021": TOYOTA.CHR_TSS2,
  "TOYOTA COROLLA 2017": TOYOTA.COROLLA,
  "TOYOTA COROLLA TSS2 2019": TOYOTA.COROLLA_TSS2,
  "TOYOTA HIGHLANDER 2017": TOYOTA.HIGHLANDER,
  "TOYOTA HIGHLANDER 2020": TOYOTA.HIGHLANDER_TSS2,
  "TOYOTA PRIUS 2017": TOYOTA.PRIUS,
  "TOYOTA PRIUS v 2017": TOYOTA.PRIUS_V,
  "TOYOTA PRIUS TSS2 2021": TOYOTA.PRIUS_TSS2,
  "TOYOTA RAV4 2017": TOYOTA.RAV4,
  "TOYOTA RAV4 HYBRID 2017": TOYOTA.RAV4H,
  "TOYOTA RAV4 2019": TOYOTA.RAV4_TSS2,
  "TOYOTA RAV4 2022": TOYOTA.RAV4_TSS2_2022,
  "TOYOTA RAV4 2023": TOYOTA.RAV4_TSS2_2023,
  "TOYOTA MIRAI 2021": TOYOTA.MIRAI,
  "TOYOTA SIENNA 2018": TOYOTA.SIENNA,
  "LEXUS CT HYBRID 2018": TOYOTA.LEXUS_CTH,
  "LEXUS ES 2018": TOYOTA.LEXUS_ES,
  "LEXUS ES 2019": TOYOTA.LEXUS_ES_TSS2,
  "LEXUS IS 2018": TOYOTA.LEXUS_IS,
  "LEXUS IS 2023": TOYOTA.LEXUS_IS_TSS2,
  "LEXUS NX 2018": TOYOTA.LEXUS_NX,
  "LEXUS NX 2020": TOYOTA.LEXUS_NX_TSS2,
  "LEXUS LC 2024": TOYOTA.LEXUS_LC_TSS2,
  "LEXUS RC 2020": TOYOTA.LEXUS_RC,
  "LEXUS RX 2016": TOYOTA.LEXUS_RX,
  "LEXUS RX 2020": TOYOTA.LEXUS_RX_TSS2,
  "LEXUS GS F 2016": TOYOTA.LEXUS_GS_F,
  "VOLKSWAGEN ARTEON 1ST GEN": VW.ARTEON_MK1,
  "VOLKSWAGEN ATLAS 1ST GEN": VW.ATLAS_MK1,
  "VOLKSWAGEN CADDY 3RD GEN": VW.CADDY_MK3,
  "VOLKSWAGEN CRAFTER 2ND GEN": VW.CRAFTER_MK2,
  "VOLKSWAGEN GOLF 7TH GEN": VW.GOLF_MK7,
  "VOLKSWAGEN JETTA 7TH GEN": VW.JETTA_MK7,
  "VOLKSWAGEN PASSAT 8TH GEN": VW.PASSAT_MK8,
  "VOLKSWAGEN PASSAT NMS": VW.PASSAT_NMS,
  "VOLKSWAGEN POLO 6TH GEN": VW.POLO_MK6,
  "VOLKSWAGEN SHARAN 2ND GEN": VW.SHARAN_MK2,
  "VOLKSWAGEN TAOS 1ST GEN": VW.TAOS_MK1,
  "VOLKSWAGEN T-CROSS 1ST GEN": VW.TCROSS_MK1,
  "VOLKSWAGEN TIGUAN 2ND GEN": VW.TIGUAN_MK2,
  "VOLKSWAGEN TOURAN 2ND GEN": VW.TOURAN_MK2,
  "VOLKSWAGEN TRANSPORTER T6.1": VW.TRANSPORTER_T61,
  "VOLKSWAGEN T-ROC 1ST GEN": VW.TROC_MK1,
  "AUDI A3 3RD GEN": VW.AUDI_A3_MK3,
  "AUDI Q2 1ST GEN": VW.AUDI_Q2_MK1,
  "AUDI Q3 2ND GEN": VW.AUDI_Q3_MK2,
  "SEAT ATECA 1ST GEN": VW.SEAT_ATECA_MK1,
  "SEAT LEON 3RD GEN": VW.SEAT_LEON_MK3,
  "SKODA FABIA 4TH GEN": VW.SKODA_FABIA_MK4,
  "SKODA KAMIQ 1ST GEN": VW.SKODA_KAMIQ_MK1,
  "SKODA KAROQ 1ST GEN": VW.SKODA_KAROQ_MK1,
  "SKODA KODIAQ 1ST GEN": VW.SKODA_KODIAQ_MK1,
  "SKODA OCTAVIA 3RD GEN": VW.SKODA_OCTAVIA_MK3,
  "SKODA SCALA 1ST GEN": VW.SKODA_SCALA_MK1,
  "SKODA SUPERB 3RD GEN": VW.SKODA_SUPERB_MK3,
}
