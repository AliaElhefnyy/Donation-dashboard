def calculate_kpis(donations, projects, volunteers):
    total_donations = donations['donation_amount'].sum()
    total_volunteers = volunteers['volunteer_name'].nunique()
    total_hours = volunteers['hours_contributed'].sum()
    total_beneficiaries = projects['beneficiaries'].sum()
    
    return {
        "total_donations": total_donations,
        "total_volunteers": total_volunteers,
        "total_hours": total_hours,
        "total_beneficiaries": total_beneficiaries
    }
