import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Commitment, PageResponse } from "@/utils/types";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { formatDigitValue } from "@/utils/utils";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"

async function fetchCommitments(commitmentId: string, page?: string, filter?: string): Promise<PageResponse<Commitment>> {
    const response = await fetch(`http://localhost:8000/api/v1/investors/${commitmentId}/commitments?size=10&page=${page || 0}&asset_class=${filter || 'all'}`)
    if (!response.ok) {
        throw new Error('An error occured when fetching the data')
    }
    return response.json()
}

export default async function CommitmentsPage({ params, searchParams }: { searchParams: { page: string | undefined , assetClass: string | undefined },
    params: { commitmentId: string , investorName: string} }) {
    
    // Next.js complains if these params are not 'awaited'
    const { commitmentId } = await params
    const { page, assetClass: filter } = await searchParams
    
    const data = await fetchCommitments(commitmentId, page, filter)

    const currentPage = data['page_number']
    const maxPageNumber = data['total_pages']
    const amountByAsset = data['content_meta']['total_commitments_per_asset_class']
    const totalCommitment = data['content_meta']['total_commitment']
    const investorName = data['content_meta']['investor_name']

    const baseRoute = `/investors/commitments/${commitmentId}`

    return (
        <main className="flex flex-col justify-center h-full text-center gap-6 max-w-5xl mx-auto my-12">
            <div className="flex justify-between">
                <h1 className="text-3xl font-semibold">
                    {investorName}
                </h1>
                <Button className="m-0.5 bg-blue-500">
                    <Link href={`/dashboard`}>
                        <span>Return to Dashboard</span>
                    </Link>
                </Button>

            </div>

            <div className="flex flex-col ">
                <Button className="m-0.5 bg-green-800">
                    <Link href={`${baseRoute}?page=0`}>
                        <span>All</span> | <span>£{formatDigitValue(totalCommitment)}</span>
                    </Link>
                </Button>
            </div>

            <div>
                {Object.keys(amountByAsset).map((asset, idx) => {
                    return (
                        <Button key={idx} className="m-0.5 bg-blue-800">
                            <Link href={`${baseRoute}?page=0&assetClass=${asset}`}>
                                <span>{asset}</span> | <span>£{formatDigitValue(amountByAsset[asset])}</span>
                            </Link>
                        </Button>
                    )
                })}
            </div>
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead className="gap-6">Commitment ID</TableHead>
                        <TableHead>Asset Class</TableHead>
                        <TableHead>Currency</TableHead>
                        <TableHead>Amount</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {data.content.map((item: Commitment) => (
                        <TableRow key={item.commitment_id}>
                            <TableCell className="text-left">{item.commitment_id}</TableCell>
                            <TableCell className="text-left">{item.commitment_asset_class}</TableCell>
                            <TableCell className="text-left">{item.commitment_currency}</TableCell>
                            <TableCell className="text-left">{formatDigitValue(item.commitment_amount)}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>

            <ul className="flex justify-between items-center text-sm mt-8">
                <li>
                    {currentPage > 0 && (
                        <Link href={`${baseRoute}?page=${currentPage - 1}&assetClass=${filter || 'all'}`}>
                            <span className="flex items-center gap-1">
                                <ChevronLeft className="w-5 h-5" />
                                Previous Page
                            </span>
                        </Link>
                    )}
                </li>


                <li className="flex-grow flex justify-center">
                    <ul className="flex items-center gap-3">
                        {[...new Array(maxPageNumber)].map((_, idx) => (
                            <li key={idx}>
                                <Button asChild size='sm' className={(currentPage == idx) ? "bg-zinc-400 h-auto px-2.5 py-1" : "h-auto px-2.5 py-1"}>
                                    <Link href={`${baseRoute}?page=${idx}&assetClass=${filter || 'all'}`}>
                                        {idx + 1}
                                    </Link>

                                </Button>
                            </li>
                        ))}


                    </ul>
                </li>

                <li>
                    {currentPage < maxPageNumber - 1 && (
                        <Link href={`${baseRoute}?page=${currentPage + 1}&assetClass=${filter || 'all'}`}>
                            <span className="flex items-center gap-1">
                                Next Page
                                <ChevronRight className="w-5 h-5" />
                            </span>
                        </Link>
                    )}
                </li>

            </ul>
        </main>

    );
}
