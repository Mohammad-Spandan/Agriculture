import logging
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Logging Configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# 1. Database Configuration
DB_USER = "root"
DB_PASS = "password"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "agriculture"

DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_engine(DATABASE_URI, echo=False)


# 2. Transformation Cleansers
def clean_fiscal_year(series: pd.Series) -> pd.Series:
  return (
      series.astype(str)
      .str.replace(r"\(p\)", "", regex=True)
      .str.replace(r"-2k$", "-00", regex=True)
      .str.strip()
  )


def clean_strings(df: pd.DataFrame, str_cols: list) -> pd.DataFrame:
  for col in str_cols:
    if col in df.columns:
      df[col] = df[col].astype(str).str.strip()
  return df


def clean_numerics(
    df: pd.DataFrame, num_cols: list, precision: int = 2
) -> pd.DataFrame:
  for col in num_cols:
    if col in df.columns:
      df[col] = (
          pd.to_numeric(df[col], errors="coerce").fillna(0.0).round(precision)
      )
  return df


# 3. Extraction Functions
def extract_soil_types() -> pd.DataFrame:
  return pd.DataFrame([
      {"soil_type_id": 1, "soil_type_name": "Non-calcareous brown"},
      {"soil_type_id": 2, "soil_type_name": "Non-calcareous alluvium"},
      {"soil_type_id": 3, "soil_type_name": "Non-calcareous grey"},
      {"soil_type_id": 4, "soil_type_name": "Non-calcareous dark grey"},
      {"soil_type_id": 5, "soil_type_name": "Acid basin clays"},
      {"soil_type_id": 6, "soil_type_name": "Calcareous alluvium"},
      {"soil_type_id": 7, "soil_type_name": "Calcareous grey"},
      {"soil_type_id": 8, "soil_type_name": "Calcareous alluvium (non-saline)"},
      {"soil_type_id": 9, "soil_type_name": "Shallow grey terrace"},
      {"soil_type_id": 10, "soil_type_name": "Deep grey terrace"},
      {"soil_type_id": 11, "soil_type_name": "Brown hill"},
      {"soil_type_id": 12, "soil_type_name": "Deep red-brown terrace"},
  ])


def extract_districts() -> pd.DataFrame:
  districts = [
      "Dhaka",
      "Gazipur",
      "Mymensinh",
      "Jamalpur",
      "Sherpur",
      "Netrokona",
      "Tangail",
      "Sylhet",
      "Habiganj",
      "Moulvibazar",
      "Sunamganj",
      "Chattogram",
      "Coxs_Bazar",
      "Bandarban",
      "Rangamati",
      "Khagrachhari",
      "Cumilla",
      "Feni",
      "Bagerhat",
      "Khulna",
      "Satkhira",
      "Rangpur",
      "Nilphamari",
      "Kurigram",
      "Lalmonirhat",
      "Dinajpur",
      "Thakurgaon",
      "Panchagarh",
      "Naogaon",
      "Noakhali",
      "Luxmipur",
      "Patuakhali",
      "Barguna",
      "Firojpur",
      "Bhola",
  ]
  return pd.DataFrame([
      {"district_id": idx + 1, "district_name": name}
      for idx, name in enumerate(districts)
  ])


def extract_agro_ecological_zones() -> pd.DataFrame:
  return pd.DataFrame([
      {
          "aez_id": 1,
          "zone_name": "Old Himalayan Piedmont Plain",
          "area_sqkm": 4008.00,
          "soil_type_id": 1,
          "sand_pct": 10.00,
          "alluvium_pct": 82.00,
          "clay_pct": 8.00,
      },
      {
          "aez_id": 2,
          "zone_name": "Tista Active",
          "area_sqkm": 836.00,
          "soil_type_id": 2,
          "sand_pct": 41.00,
          "alluvium_pct": 59.00,
          "clay_pct": 0.00,
      },
      {
          "aez_id": 3,
          "zone_name": "Tista Meander Floodplain",
          "area_sqkm": 9468.00,
          "soil_type_id": 3,
          "sand_pct": 6.00,
          "alluvium_pct": 88.00,
          "clay_pct": 6.00,
      },
      {
          "aez_id": 4,
          "zone_name": "Korotoya Bangali Floodplain",
          "area_sqkm": 2572.00,
          "soil_type_id": 3,
          "sand_pct": 8.00,
          "alluvium_pct": 65.00,
          "clay_pct": 27.00,
      },
      {
          "aez_id": 5,
          "zone_name": "Lower Atrai Basin",
          "area_sqkm": 851.00,
          "soil_type_id": 4,
          "sand_pct": 0.00,
          "alluvium_pct": 16.00,
          "clay_pct": 84.00,
      },
      {
          "aez_id": 6,
          "zone_name": "Lower Punarbhaba Floodplain",
          "area_sqkm": 129.00,
          "soil_type_id": 5,
          "sand_pct": 0.00,
          "alluvium_pct": 0.00,
          "clay_pct": 100.00,
      },
  ])


def extract_forest_lands() -> pd.DataFrame:
  return pd.DataFrame([
      {
          "forest_id": 1,
          "district_id": 12,
          "reserved_forest_sqkm": 1250.40,
          "protected_forest_sqkm": 320.10,
          "unclassed_forest_sqkm": 140.50,
      },
      {
          "forest_id": 2,
          "district_id": 13,
          "reserved_forest_sqkm": 890.25,
          "protected_forest_sqkm": 180.00,
          "unclassed_forest_sqkm": 75.30,
      },
      {
          "forest_id": 3,
          "district_id": 15,
          "reserved_forest_sqkm": 2100.80,
          "protected_forest_sqkm": 450.20,
          "unclassed_forest_sqkm": 1280.00,
      },
      {
          "forest_id": 4,
          "district_id": 20,
          "reserved_forest_sqkm": 4016.00,
          "protected_forest_sqkm": 0.00,
          "unclassed_forest_sqkm": 0.00,
      },
  ])


def extract_land_utilization() -> pd.DataFrame:
  return pd.DataFrame([
      {
          "record_id": 1,
          "district_id": 1,
          "fiscal_year": "1999-2k",
          "total_area_acres": 367000.00,
          "forest_area_acres": 22000.00,
          "net_cropped_acres": 210000.00,
      },
      {
          "record_id": 2,
          "district_id": 12,
          "fiscal_year": "2004-05(p)",
          "total_area_acres": 1280000.00,
          "forest_area_acres": 340000.00,
          "net_cropped_acres": 520000.00,
      },
      {
          "record_id": 3,
          "district_id": 20,
          "fiscal_year": " 2011-12 ",
          "total_area_acres": 1085000.00,
          "forest_area_acres": 480000.00,
          "net_cropped_acres": 390000.00,
      },
  ])


# 4. Pipeline Execution
def run_etl_pipeline():
  logging.info("Starting ETL Pipeline Execution...")

  # Extract
  df_soil = extract_soil_types()
  df_districts = extract_districts()
  df_aez = extract_agro_ecological_zones()
  df_forest = extract_forest_lands()
  df_land = extract_land_utilization()

  # Transform
  df_soil = clean_strings(df_soil, ["soil_type_name"])
  df_districts = clean_strings(df_districts, ["district_name"])
  df_aez = clean_strings(df_aez, ["zone_name"])
  df_aez = clean_numerics(
      df_aez, ["area_sqkm", "sand_pct", "alluvium_pct", "clay_pct"]
  )
  df_forest = clean_numerics(
      df_forest,
      ["reserved_forest_sqkm", "protected_forest_sqkm", "unclassed_forest_sqkm"],
  )

  df_land["fiscal_year"] = clean_fiscal_year(df_land["fiscal_year"])
  df_land = clean_numerics(
      df_land, ["total_area_acres", "forest_area_acres", "net_cropped_acres"]
  )

  # Load (Respecting Dependency Hierarchy)
  tables_in_order = [
      ("soil_types", df_soil),
      ("districts", df_districts),
      ("agro_ecological_zones", df_aez),
      ("forest_lands", df_forest),
      ("land_utilization", df_land),
  ]

  try:
    with engine.begin() as conn:
      logging.info(
          "Disabling Foreign Key checks for safe staging truncation..."
      )
      conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

      for table_name, df in tables_in_order:
        logging.info(f"Staging table: {table_name} ({len(df)} records)")
        conn.execute(text(f"TRUNCATE TABLE {table_name};"))
        df.to_sql(table_name, con=conn, if_exists="append", index=False)

      logging.info("Re-enabling Foreign Key checks...")
      conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    logging.info("ETL Pipeline execution completed successfully!")
  except SQLAlchemyError as e:
    logging.error(f"ETL Pipeline execution failed: {str(e)}")
    raise e


if __name__ == "__main__":
  run_etl_pipeline()
