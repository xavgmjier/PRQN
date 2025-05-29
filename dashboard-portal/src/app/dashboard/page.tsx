import { Investor, PageResponse } from "@/utils/types";
import { formatDateValue, formatDigitValue } from "@/utils/utils";
import Link from "next/link";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"

async function fetchInvestors(): Promise<PageResponse<Investor>> {
    try {
        const response = await fetch("http://localhost:8000/api/v1/investors/")
        return response.json()
    } catch (e) {
        throw new Error('Error fetching investor dashboard data')
    }

}

export default async function Home() {

    const fetchResult = await fetchInvestors()
    const content = fetchResult.content
    const investor_total_commitment_map = fetchResult.content_meta.total_commitments

    return (

        <main className="flex flex-col justify-center h-full text-center gap-6 max-w-5xl mx-auto my-12">
            <div className="flex justify-between">
                <h1 className="text-3xl font-semibold">
                    Investors
                </h1>
            </div>
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>ID</TableHead>
                        <TableHead>Investor Name</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead>Date Added</TableHead>
                        <TableHead>Country</TableHead>
                        <TableHead>Total Commitment</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {content.map((investor: Investor) => (
                        <TableRow key={investor.investor_id}>
                            <TableCell className="text-left p-0">
                                <Link className="block p-4 font-semibold" href={`/investors/commitments/${investor.investor_id}`}>
                                    {investor.investor_id}
                                </Link>
                            </TableCell>
                            <TableCell className="text-left p-0">
                                <Link className="block p-4" href={`/investors/commitments/${investor.investor_id}`}>
                                    {investor.investor_name}
                                </Link>
                            </TableCell>
                            <TableCell className="text-left p-0">
                                <Link className="block p-4" href={`/investors/commitments/${investor.investor_id}`}>
                                    {investor.investory_type}
                                </Link>
                            </TableCell>
                            <TableCell className="text-left p-0">
                                <Link className="block p-4" href={`/investors/commitments/${investor.investor_id}`}>
                                    {formatDateValue(investor.investor_date_added)}
                                </Link>
                            </TableCell>
                            <TableCell className="text-left p-0">
                                <Link className="block p-4" href={`/investors/commitments/${investor.investor_id}`}>
                                    {investor.investor_country}
                                </Link>
                            </TableCell>
                            <TableCell className="text-center p-0">
                                <Link className="block p-4 font-semibold" href={`/investors/commitments/${investor.investor_id}`}>
                                    {formatDigitValue(investor_total_commitment_map[investor.investor_id])}
                                </Link>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </main>

    );
}
