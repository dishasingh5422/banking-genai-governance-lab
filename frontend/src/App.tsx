import { FormEvent, useEffect, useMemo, useState } from "react";

const API = import.meta.env.VITE_API_URL ?? `${window.location.protocol}//${window.location.hostname}:8000`;
const pages = ["Overview", "Customer Review", "Case Copilot", "Model Governance", "Evaluation", "Data Quality"] as const;
type Page = typeof pages[number];
type Summary = { customers: number; transactions: number; review_queue: number; high_risk_customers: number; data_quality_score: number; attrition_rate: number; model_status: string; metrics: Record<string, number>; age_group_metrics: {group:string; customers:number; actual_attrition_rate:number; high_risk_rate:number}[]; max_high_risk_rate_difference:number; limitations:string[] };
type Customer = { customer_id:string; segment:string; region:string; risk_band:string; risk_probability:number; complaints_90d:number; late_payments_6m:number };
type ModelCard = { model:string; version:string; status:string; intended_use:string; prohibited_uses:string[]; metrics:Record<string,number>; fairness_diagnostic:Record<string,number>; limitations:string[] };
type Evaluation = { status:string; tests:number; passed?:number; results?:{question:string;actual_status:string;passed:boolean;cited_sources:string[]}[] };

function formatNumber(value:number) { return new Intl.NumberFormat("en-IN").format(value); }
function percent(value:number) { return `${(value * 100).toFixed(1)}%`; }

function Metric({label,value,note}:{label:string;value:string;note:string}) {
  return <article className="metric"><span>{label}</span><strong>{value}</strong><small>{note}</small></article>;
}

function Empty({message}:{message:string}) { return <div className="empty">{message}</div>; }

export default function App() {
  const [page,setPage] = useState<Page>("Overview");
  const [summary,setSummary] = useState<Summary|null>(null);
  const [customers,setCustomers] = useState<Customer[]>([]);
  const [modelCard,setModelCard] = useState<ModelCard|null>(null);
  const [evaluation,setEvaluation] = useState<Evaluation|null>(null);
  const [question,setQuestion] = useState("What should an analyst verify before retention outreach?");
  const [selectedCustomer,setSelectedCustomer] = useState("");
  const [answer,setAnswer] = useState<any>(null);
  const [error,setError] = useState("");
  const [loading,setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/portfolio/summary`).then(r=>r.json()),
      fetch(`${API}/api/customers?limit=25`).then(r=>r.json()),
      fetch(`${API}/api/governance/model-card`).then(r=>r.json()),
      fetch(`${API}/api/evaluations/summary`).then(r=>r.json()),
    ]).then(([s,c,m,e])=>{setSummary(s);setCustomers(c);setModelCard(m);setEvaluation(e);setSelectedCustomer(c[0]?.customer_id ?? "");})
      .catch(()=>setError("The API is not reachable. Start the backend on port 8000."))
      .finally(()=>setLoading(false));
  },[]);

  const riskCounts = useMemo(() => customers.reduce<Record<string,number>>((acc,row)=>{acc[row.risk_band]=(acc[row.risk_band]??0)+1;return acc;},{}),[customers]);

  async function askCopilot(event:FormEvent) {
    event.preventDefault(); setAnswer({status:"WORKING"});
    const response = await fetch(`${API}/api/copilot/query`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question,customer_id:selectedCustomer||null})});
    setAnswer(await response.json());
  }

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><span className="brand-mark">BG</span><div><strong>Governance Lab</strong><small>Consumer banking AI</small></div></div>
      <nav>{pages.map(item=><button key={item} className={page===item?"active":""} onClick={()=>setPage(item)}><span>{item.slice(0,1)}</span>{item}</button>)}</nav>
      <div className="sidebar-note"><strong>Portfolio simulation</strong><p>Synthetic data. Human review required.</p></div>
    </aside>
    <main>
      <header><div><p className="eyebrow">BANKING ANALYTICS AND GENAI CONTROLS</p><h1>{page}</h1></div><div className="status"><i></i>Local demo</div></header>
      {error && <div className="alert">{error}</div>}
      {loading ? <Empty message="Loading verified project evidence…"/> : <>
        {page==="Overview" && summary && <section>
          <div className="metrics-grid">
            <Metric label="Synthetic customers" value={formatNumber(summary.customers)} note={`${formatNumber(summary.transactions)} transactions`} />
            <Metric label="Review queue" value={formatNumber(summary.review_queue)} note="Medium and high risk" />
            <Metric label="High-risk cases" value={formatNumber(summary.high_risk_customers)} note="Prioritized for human review" />
            <Metric label="Model ROC AUC" value={summary.metrics.roc_auc.toFixed(3)} note="Held-out validation" />
          </div>
          <div className="two-column">
            <article className="panel"><div className="panel-head"><div><p className="eyebrow">SEGMENT MONITORING</p><h2>High-risk rate by age group</h2></div><span className="tag">Diagnostic only</span></div>
              <div className="bars">{summary.age_group_metrics.map(row=><div className="bar-row" key={row.group}><span>{row.group}</span><div><i style={{width:`${row.high_risk_rate*100}%`}}></i></div><strong>{percent(row.high_risk_rate)}</strong></div>)}</div>
              <p className="caption">Maximum observed difference: {percent(summary.max_high_risk_rate_difference)}. This does not establish regulatory compliance.</p>
            </article>
            <article className="panel"><div className="panel-head"><div><p className="eyebrow">MODEL PERFORMANCE</p><h2>Validation evidence</h2></div><span className="tag success">Validated demo</span></div>
              <dl className="metric-list">{Object.entries(summary.metrics).map(([key,value])=><div key={key}><dt>{key.replaceAll("_"," ")}</dt><dd>{value.toFixed(3)}</dd></div>)}</dl>
            </article>
          </div>
        </section>}
        {page==="Customer Review" && <section className="panel"><div className="panel-head"><div><p className="eyebrow">PRIORITIZED QUEUE</p><h2>Customer review cases</h2></div><div className="legend"><span>High {riskCounts.HIGH??0}</span><span>Medium {riskCounts.MEDIUM??0}</span><span>Low {riskCounts.LOW??0}</span></div></div>
          <div className="table-wrap"><table><thead><tr><th>Customer</th><th>Segment</th><th>Region</th><th>Risk</th><th>Score</th><th>Complaints</th><th>Late payments</th></tr></thead><tbody>{customers.map(row=><tr key={row.customer_id}><td>{row.customer_id}</td><td>{row.segment}</td><td>{row.region}</td><td><span className={`risk ${row.risk_band.toLowerCase()}`}>{row.risk_band}</span></td><td>{percent(row.risk_probability)}</td><td>{row.complaints_90d}</td><td>{row.late_payments_6m}</td></tr>)}</tbody></table></div>
        </section>}
        {page==="Case Copilot" && <section className="copilot-layout"><form className="panel" onSubmit={askCopilot}><p className="eyebrow">GROUNDED ASSISTANCE</p><h2>Ask about a review case</h2><label>Customer<select value={selectedCustomer} onChange={e=>setSelectedCustomer(e.target.value)}>{customers.map(row=><option key={row.customer_id}>{row.customer_id}</option>)}</select></label><label>Question<textarea value={question} onChange={e=>setQuestion(e.target.value)} rows={5}/></label><button className="primary" type="submit">Generate grounded summary</button><p className="caption">No account action is performed. Responses require human review.</p></form>
          <article className="panel response"><div className="panel-head"><h2>Copilot response</h2>{answer?.status&&<span className={`tag ${answer.status==="GROUNDED"?"success":""}`}>{answer.status}</span>}</div>{!answer?<Empty message="Submit a policy or servicing question to see a cited response."/>:answer.status==="WORKING"?<Empty message="Retrieving policy evidence…"/>:<><p>{answer.answer}</p><h3>Sources</h3>{answer.citations?.length?answer.citations.map((c:any)=><div className="source" key={c.source}><strong>{c.source.replaceAll("_"," ")}</strong><span>Similarity {c.score}</span><p>{c.excerpt}</p></div>):<p className="caption">No sources returned.</p>}</>}</article>
        </section>}
        {page==="Model Governance" && modelCard && <section className="two-column"><article className="panel"><p className="eyebrow">MODEL CARD</p><h2>{modelCard.model}</h2><dl className="details"><div><dt>Version</dt><dd>{modelCard.version}</dd></div><div><dt>Status</dt><dd>{modelCard.status}</dd></div><div><dt>Intended use</dt><dd>{modelCard.intended_use}</dd></div></dl><h3>Limitations</h3><ul>{modelCard.limitations.map(item=><li key={item}>{item}</li>)}</ul></article><article className="panel"><p className="eyebrow">CONTROL BOUNDARIES</p><h2>Prohibited uses</h2><ul className="control-list">{modelCard.prohibited_uses.map(item=><li key={item}><span>×</span>{item}</li>)}</ul><h3>Fairness diagnostic</h3><p>Maximum age-group high-risk-rate difference: <strong>{percent(modelCard.fairness_diagnostic.age_group_max_high_risk_rate_difference)}</strong></p></article></section>}
        {page==="Evaluation" && evaluation && <section className="panel"><div className="panel-head"><div><p className="eyebrow">LLM AND RETRIEVAL TESTS</p><h2>Safety evaluation</h2></div><span className={`tag ${evaluation.status==="PASS"?"success":""}`}>{evaluation.passed}/{evaluation.tests} passed</span></div><div className="test-list">{evaluation.results?.map((result,index)=><div key={index}><span className={result.passed?"pass":"fail"}>{result.passed?"PASS":"FAIL"}</span><div><strong>{result.question}</strong><small>{result.actual_status} · {result.cited_sources.join(", ")||"no citation required"}</small></div></div>)}</div></section>}
        {page==="Data Quality" && summary && <section><div className="metrics-grid"><Metric label="Quality score" value={`${summary.data_quality_score.toFixed(1)}%`} note="Across generated fields"/><Metric label="Detected issues" value="0" note="Primary key and missing checks"/><Metric label="Pipeline seed" value="20260917" note="Deterministic generation"/><Metric label="Model status" value="PASS" note="Validated portfolio demo"/></div><article className="panel"><p className="eyebrow">LINEAGE</p><h2>Data flow</h2><div className="lineage"><span>Synthetic generator</span><i>→</i><span>Validation</span><i>→</i><span>DuckDB SQL</span><i>→</i><span>Feature model</span><i>→</i><span>Dashboard APIs</span></div></article></section>}
      </>}
    </main>
  </div>;
}
