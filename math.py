from scipy.stats import norm

def get_z_table_value(z_score):
    """Return cumulative probability for a given z-score."""
    return norm.cdf(z_score)


z = float(input("Enter a Z-score (e.g., 1.23): "))
value = get_z_table_value(z)
print(f"Z-table value for z = {z}: {value:.5f}")