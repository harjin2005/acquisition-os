import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import { apiGet, apiPost, mintDevToken } from './lib/api';

// ---------------------------------------------------------------------------
// Sprint 1 UI — deliberately minimal. This is not the product; it is the
// acceptance-visible surface for DOC-131 §2 items 1, 4, 5. Product screens
// (Today, Pipeline, Inbox, Workspaces) begin landing in E7.
// ---------------------------------------------------------------------------

function Nav() {
  return (
    <div className="row" style={{ marginBottom: 40 }}>
      <div className="stack">
        <span className="eyebrow" data-testid="app-eyebrow">AcquisitionOS · Sprint 1 · Foundation</span>
        <span className="status-line">DOC-131 §2 — Repo, CI, Terraform, WorkOS, Alembic + RLS</span>
      </div>
      <div style={{ display: 'flex', gap: 10 }}>
        <Link to="/" className="btn" data-testid="nav-home">Overview</Link>
        <Link to="/bootstrap" className="btn" data-testid="nav-bootstrap">Bootstrap Org</Link>
        <Link to="/console" className="btn" data-testid="nav-console">Console</Link>
      </div>
    </div>
  );
}

function Overview() {
  const health = useQuery({
    queryKey: ['health'],
    queryFn: () => apiGet('/api/health'),
    refetchInterval: 6000,
  });
  const sprint = useQuery({ queryKey: ['sprint'], queryFn: () => apiGet('/api/meta/sprint') });

  const ok = health.data?.status === 'ok';

  return (
    <>
      <span className="eyebrow">Milestone M1 (end Sprint 2)</span>
      <h1 className="hero" data-testid="hero">
        Foundation shipped. <em>Product features begin next sprint.</em>
      </h1>
      <p className="lede">
        This build closes the six Sprint 1 acceptance criteria from DOC-131 §2. Nothing here is customer-facing —
        Sprint 1 exists so the next 17 sprints can proceed with a boundary-enforced, RLS-verified, secret-safe substrate.
      </p>

      <div className="divider" />

      <div className="row" style={{ marginBottom: 20 }}>
        <div className="stack">
          <span className="eyebrow">Health</span>
          <div>
            <span className={`dot ${ok ? 'ok' : 'err'}`} />
            <span className="mono" data-testid="health-status">
              {health.isLoading ? 'checking…' : ok ? `api ${health.data.version} · ${health.data.env}` : 'unhealthy'}
            </span>
          </div>
        </div>
        <div className="stack" style={{ alignItems: 'flex-end' }}>
          <span className="tag">v{health.data?.version || '—'}</span>
          <span className="tag">env: {health.data?.env || '—'}</span>
        </div>
      </div>

      <div className="card">
        <span className="eyebrow">Sprint 1 · Acceptance Criteria</span>
        <h3 style={{ margin: '4px 0 12px', fontFamily: 'var(--font-body)' }}>{sprint.data?.objective || '—'}</h3>
        {sprint.data?.acceptance_criteria?.map((ac) => (
          <div key={ac.id} className="progress-row" data-testid={`ac-${ac.id}`}>
            <div className={`check ${ac.met ? 'done' : ''}`}>{ac.met ? '✓' : '·'}</div>
            <div>{ac.title}</div>
            <div className="tag">{ac.id}</div>
          </div>
        ))}
      </div>

      <div className="footer">
        <div>Documentation is the contract. Implementation follows.</div>
        <div>
          <a href="/api/docs" target="_blank" rel="noreferrer">/api/docs</a> · &nbsp;
          <a href="/api/health" target="_blank" rel="noreferrer">/api/health</a> · &nbsp;
          <a href="/api/meta/sprint" target="_blank" rel="noreferrer">/api/meta/sprint</a>
        </div>
      </div>
    </>
  );
}

function Bootstrap() {
  const nav = useNavigate();
  const [name, setName] = React.useState('Design Partners Co');
  const [slug, setSlug] = React.useState('design-partners-co');
  const [err, setErr] = React.useState(null);
  const [busy, setBusy] = React.useState(false);

  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setErr(null);
    try {
      const res = await apiPost('/api/v1/identity/orgs', { name, slug });
      const token = mintDevToken({
        subject_id: res.founder.subject_id,
        org_id: res.org.id,
        role: 'OWNER',
        email: res.founder.email,
      });
      window.localStorage.setItem('aos.session', JSON.stringify({ ...res, token }));
      nav('/console');
    } catch (e) {
      setErr(String(e.message || e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <span className="eyebrow">Identity · A1 · bootstrap</span>
      <h1 className="hero" data-testid="bootstrap-hero">
        Create the first organization.
      </h1>
      <p className="lede">
        Sprint 1 dev path: this stands in for the WorkOS provisioning webhook (E1 tail). The founder becomes the
        <em> owner</em>. RLS binds every subsequent request to this org's id via <code>SET LOCAL app.org_id</code>.
      </p>

      <form className="card" onSubmit={submit} style={{ marginTop: 24 }}>
        <div className="stack" style={{ gap: 8, marginBottom: 12 }}>
          <label className="eyebrow" htmlFor="name">Organization name</label>
          <input
            id="name"
            data-testid="bootstrap-name-input"
            className="input"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="stack" style={{ gap: 8, marginBottom: 12 }}>
          <label className="eyebrow" htmlFor="slug">Slug (a-z 0-9 -)</label>
          <input
            id="slug"
            data-testid="bootstrap-slug-input"
            className="input"
            value={slug}
            pattern="^[-a-z0-9]+$"
            onChange={(e) => setSlug(e.target.value)}
            required
          />
        </div>
        {err && <div className="error" data-testid="bootstrap-error">{err}</div>}
        <div className="row" style={{ marginTop: 16 }}>
          <span className="status-line">Idempotent by slug — retry-safe.</span>
          <button type="submit" className="btn primary" data-testid="bootstrap-submit" disabled={busy}>
            {busy ? 'Provisioning…' : 'Create organization'}
          </button>
        </div>
      </form>
    </>
  );
}

function Console() {
  const session = React.useMemo(() => {
    try { return JSON.parse(window.localStorage.getItem('aos.session') || 'null'); } catch { return null; }
  }, []);

  const membersQ = useQuery({
    queryKey: ['members', session?.org?.id],
    queryFn: () => apiGet('/api/v1/identity/orgs/me/members', session?.token),
    enabled: !!session,
  });

  const [inviteEmail, setInviteEmail] = React.useState('');
  const [inviteRole, setInviteRole] = React.useState('member');
  const [inviteResult, setInviteResult] = React.useState(null);
  const [inviteErr, setInviteErr] = React.useState(null);

  async function invite(e) {
    e.preventDefault();
    setInviteErr(null);
    try {
      const res = await apiPost('/api/v1/identity/orgs/me/invites', { email: inviteEmail, role: inviteRole }, session.token);
      setInviteResult(res);
      setInviteEmail('');
      membersQ.refetch();
    } catch (e) {
      setInviteErr(String(e.message || e));
    }
  }

  if (!session) {
    return (
      <>
        <span className="eyebrow">Console</span>
        <h1 className="hero">No org yet.</h1>
        <p className="lede">Bootstrap an organization first.</p>
        <Link to="/bootstrap" className="btn primary" data-testid="console-bootstrap-cta">Bootstrap Org</Link>
      </>
    );
  }

  return (
    <>
      <span className="eyebrow">Identity · Console</span>
      <h1 className="hero" data-testid="console-hero">{session.org.name}</h1>
      <p className="lede">
        Slug <code>{session.org.slug}</code> · org id <code className="mono">{session.org.id.slice(0, 8)}…</code>
      </p>

      <div className="divider" />

      <div className="card">
        <div className="row">
          <span className="eyebrow">Members</span>
          <span className="tag">{membersQ.data?.length ?? 0} active</span>
        </div>
        <div style={{ marginTop: 12 }}>
          {membersQ.isLoading && <span className="status-line">loading…</span>}
          {membersQ.data?.map((m) => (
            <div key={m.id} className="progress-row" data-testid={`member-${m.id}`}>
              <div className="check done">·</div>
              <div>
                <div>{m.email}</div>
                <div className="status-line">{m.role} · {m.status}</div>
              </div>
              <div className="tag">{m.role}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <span className="eyebrow">Invite a member</span>
        <form className="grid" style={{ marginTop: 12 }} onSubmit={invite}>
          <input
            className="input"
            data-testid="invite-email-input"
            placeholder="teammate@example.com"
            value={inviteEmail}
            onChange={(e) => setInviteEmail(e.target.value)}
            required
            type="email"
          />
          <select
            className="input"
            data-testid="invite-role-select"
            value={inviteRole}
            onChange={(e) => setInviteRole(e.target.value)}
          >
            <option value="viewer">viewer</option>
            <option value="member">member</option>
            <option value="manager">manager</option>
            <option value="admin">admin</option>
          </select>
          <button type="submit" className="btn primary" style={{ gridColumn: '1 / span 2' }} data-testid="invite-submit">
            Send invite
          </button>
          {inviteErr && <div className="error" style={{ gridColumn: '1 / span 2' }} data-testid="invite-error">{inviteErr}</div>}
        </form>
        {inviteResult && (
          <div className="status-line" style={{ marginTop: 12 }} data-testid="invite-result">
            invite created · token starts with <code className="mono">{inviteResult.token.slice(0, 8)}…</code> · role{' '}
            <span className="tag">{inviteResult.role}</span>
          </div>
        )}
      </div>

      <div className="card">
        <span className="eyebrow">Session (dev)</span>
        <div className="status-line" style={{ marginTop: 8 }}>
          Role: <span className="tag">owner</span> — RLS binds every request to this org's id via
          <code> SET LOCAL app.org_id</code>. In staging/prod, WorkOS JWTs replace this dev token
          (see <code>ADR-EMERGENT-001</code>).
        </div>
      </div>
    </>
  );
}

export default function App() {
  return (
    <div className="container">
      <Nav />
      <Routes>
        <Route path="/" element={<Overview />} />
        <Route path="/bootstrap" element={<Bootstrap />} />
        <Route path="/console" element={<Console />} />
      </Routes>
    </div>
  );
}
