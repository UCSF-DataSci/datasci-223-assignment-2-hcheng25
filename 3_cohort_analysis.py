import polars as pl

def analyze_patient_cohorts(input_file: str) -> pl.DataFrame:
    """
    Analyze patient cohorts based on BMI ranges.
    
    Args:
        input_file: Path to the input CSV file
        
    Returns:
        DataFrame containing cohort analysis results with columns:
        - bmi_range: The BMI range (e.g., "Underweight", "Normal", "Overweight", "Obese")
        - avg_glucose: Mean glucose level by BMI range
        - patient_count: Number of patients by BMI range
        - avg_age: Mean age by BMI range
    """
    # Convert CSV to Parquet for efficient processing
    pl.read_csv(input_file).write_parquet("patients_large.parquet")
    
    # Create a lazy query to analyze cohorts
    cohort_results = pl.scan_parquet("patients_large.parquet").pipe(
        lambda df: df.filter((pl.col("BMI") >= 10) & (pl.col("BMI") <= 60))
    ).pipe(
        lambda df: df.select(["BMI", "Glucose", "Age"])
    ).pipe(
        lambda df: df.with_columns(
            pl.col("BMI").cut(
                breaks=[18.5, 25, 30], # removed 10 and 60 as breaks, because it was inducing an error, and the filter in line 22 should already mean that 10 and 60 are the min/max
                labels=["Underweight", "Normal", "Overweight", "Obese"],
                left_closed=True
            ).alias("bmi_range")
        )
    ).pipe(
        lambda df: df.group_by("bmi_range").agg([ # changed groupby to group_by
            pl.col("Glucose").mean().alias("avg_glucose"),
            pl.count().alias("patient_count"),
            pl.col("Age").mean().alias("avg_age")
        ])
    ).collect(streaming=True)
    
    return cohort_results

def main():
    # Input file
    input_file = "patients_large.csv"
    
    # Run analysis
    results = analyze_patient_cohorts(input_file)
    
    # Print summary statistics
    print("\nCohort Analysis Results:") # Changed from Summary to Results
    print(results)

if __name__ == "__main__":
    main() 