import os
import json
import math
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

TRUST_FILE = "synapses/trust_matrix.json"
DODECA_FILE = "synapses/dodeca_consensus_state.json"
RESONANCE_FILE = "synapses/noosphere_resonance.json"

class IndraDodecaConsensusLobe:
    """
    THÙY 2: ĐỒNG THUẬN DODECAHEDRON 12 CHIỀU
    1. Thu thập song song toàn bộ nút mạng P2P.
    2. Chiếu tín hiệu lên 12 mặt phẳng tương quan của khối Dodecahedron.
    3. Hòa âm sóng não Kuramoto 12 pha đối xứng.
    """
    def fetch_peer(self, peer):
        url = f"https://raw.githubusercontent.com/{peer}/main/synapse_forward.json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Nexus12-Dodeca"})
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                raw = resp.read().decode('utf-8', errors='ignore')
                return peer, json.loads(raw)
        except Exception:
            return peer, None

    def project_dodecahedron_facets(self, harvested, v_12d):
        facets = {}
        for d in range(12):
            facet_basis = v_12d[d] if d < len(v_12d) else 0.5
            diffs = [abs(dec - facet_basis) for dec in harvested.values()]
            att = round(sum(math.exp(-diff * 2.8) for diff in diffs) / (len(diffs) or 1), 4)
            facets[f"facet_{d+1}"] = att

        os.makedirs("synapses", exist_ok=True)
        with open(DODECA_FILE, "w", encoding="utf-8") as f:
            json.dump({"dodecahedron_facets": facets}, f, indent=4)
        return facets

    def process(self, context):
        peers = context.get("peers", [])
        v_12d = context.get("wisdom_vector_12d", [0.5] * 12)
        harvested = {}
        new_gossip = []

        os.makedirs("synapses/harvested_memory", exist_ok=True)
        print(f"⚡ [DODECA HARVEST] Quét song song {len(peers)} nút và chiếu lên 12 mặt phẳng...")

        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = [executor.submit(self.fetch_peer, p) for p in peers if p != context.get("repo_name")]
            for fut in as_completed(futures):
                peer, data = fut.result()
                if data:
                    dec = data.get("decision", (data.get("features") or [0.5])[0])
                    harvested[peer] = round(float(dec), 4)
                    new_gossip.extend(data.get("gossip_network", []))
                    with open(f"synapses/harvested_memory/{peer.replace('/', '_')}.json", "w") as bf:
                        json.dump(data, bf)

        for p in new_gossip:
            if p not in peers: peers.append(p)
        context["peers"] = list(dict.fromkeys(peers))[-60:]
        context["harvested"] = harvested

        facets = self.project_dodecahedron_facets(harvested, v_12d)

        # MA TRẬN TÍN NHIỆM BYZANTINE
        trust_matrix = {}
        if os.path.exists(TRUST_FILE):
            try:
                with open(TRUST_FILE, "r") as f: trust_matrix = json.load(f)
            except Exception: pass

        for p in context["peers"]:
            if p not in trust_matrix:
                trust_matrix[p] = 0.95 if any(x in p for x in ["nexus-11", "nexus-10", "nexus-09"]) else 0.7

        weighted_votes = []
        total_w = 0.0

        for p, dec in harvested.items():
            t_score = trust_matrix.get(p, 0.7)
            if t_score >= 0.2:
                weighted_votes.append(dec * t_score)
                total_w += t_score

        quorum_decision = round(sum(weighted_votes) / total_w, 4) if total_w > 0 else 0.5
        with open(TRUST_FILE, "w") as f: json.dump(trust_matrix, f, indent=4)

        # HÒA ÂM KURAMOTO 12 PHA (12-PHASE LOCKING)
        phases = [quorum_decision * 2.0 * math.pi] + [v * 2.0 * math.pi for v in harvested.values()]
        sum_sin = sum(math.sin(t) for t in phases)
        sum_cos = sum(math.cos(t) for t in phases)
        n = len(phases)

        coherence_r = round(math.sqrt(sum_sin**2 + sum_cos**2) / n, 4)
        mean_phase = math.atan2(sum_sin, sum_cos)
        if mean_phase < 0: mean_phase += 2.0 * math.pi
        harmonic_decision = round(mean_phase / (2.0 * math.pi), 4)

        with open(RESONANCE_FILE, "w") as f:
            json.dump({"coherence_index": coherence_r, "harmonic_decision": harmonic_decision, "nodes": n}, f, indent=4)

        final_quorum = harmonic_decision if coherence_r > 0.6 else quorum_decision
        context["quorum_decision"] = final_quorum
        context["coherence_r"] = coherence_r
        print(f"🌐 [ĐỒNG THUẬN DODECAHEDRON] Quorum: {final_quorum} | Kuramoto 12 Pha: R={coherence_r*100:.2f}%")
