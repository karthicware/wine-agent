SCHEMA = """
Database (MariaDB) schema contains the following tables and column descriptions:

1. Table: wl_country_group_master
Purpose: Stores master records for grouped country codes.
- cg_code: Primary key. Unique country group code. **Display: No**
- cg_name: Name of the country group. **Display: Yes**
- cg_list: Comma-separated country codes (e.g., DXB,BUD,ABJ). **Display: Yes**
- cg_isonhold: Integer (0 or 1). Indicates if this country group is on hold. **Display: Yes**
- cg_parent_code: Foreign key referencing cg_code (self-reference for parent-child relation). **Display: No**

2. Table: wl_wine_master
Purpose: Stores master list of all wines.
- WN_CODE: Primary key. Unique identifier for each wine. **Display: No**
- WN_NAME: Name of the wine. **Display: Yes**. **Like search: Yes**
- WN_TYPE: Type/category of the wine. **Display: Yes**
- WN_STATUS: Status of the wine (1 = Active, 2 = Inactive, 3 = Pending). Only status 1 is eligible for scheduling. **Display: Yes**

3. Table: wl_wine_schedule_master
Purpose: Stores details of wine scheduling across cabin classes and country groups.
- WS_ID: Primary key. Unique schedule ID. **Display: No**
- WS_CG_CODE: Foreign key referencing wl_country_group_master.cg_code. **Display: No**
- WS_WN_CODE: Foreign key referencing wl_wine_master.WN_CODE. **Display: No**
- WS_CLASS: Cabin class for the wine (First, Business, Premium Economy, Economy). **Display: Yes**
- WS_START_DATE: Start date of the wine schedule. **Display: Yes**
- WS_END_DATE: End date of the wine schedule. **Display: Yes**

4. Table: wl_cms_t_flt_wine_schedule
Purpose: Stores mapping of wines to specific flights and dates.
- CMST_FLIGHT_NO: Flight number (e.g., AC001, AC500). **Display: Yes**
- CMST_FLT_DATE: Flight date in DD-MM-YYYY format. **Display: Yes**
- CMST_WN_DEP_STN: Departure airport/station code (e.g., DXB, BOM, MAA). **Display: Yes**
- CMST_WS_CLASS: Cabin class for which wine is assigned. **Display: Yes**
- CMST_WN_CODE: Foreign key referencing wl_wine_master.WN_CODE. **Display: Yes**
- CMST_CG_NAME: Name of the associated country group. **Display: Yes**

Query Rules:
- Generate only SELECT queries. Do NOT include INSERT, UPDATE, DELETE, or DDL operations.
- Include only columns marked 'Display: Yes' in the SELECT clause.
- You MAY use columns marked 'Display: No' in WHERE, JOIN, or filtering logic.
- Apply SQL Upper function on both left and right side if column is eligible for LIKE search.
""" 