export function formatDigitValue(value: number) {
    return new Intl.NumberFormat("gb-GB", { notation: 'compact', minimumSignificantDigits: 3 }).format(value)
}

export function formatDateValue(dateString: string) {
    return new Date(dateString).toLocaleDateString('en-US', { day: 'numeric' ,month: 'long', year: 'numeric'} )
}
