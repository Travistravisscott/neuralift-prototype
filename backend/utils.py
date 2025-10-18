def compute_neurascore(focus_samples):
    if not focus_samples:
        return 0
    avg_focus = sum(focus_samples) / len(focus_samples)
    stability = 1.0 - (sum(abs(avg_focus - s) for s in focus_samples) / len(focus_samples))
    score = (avg_focus * 0.7 + stability * 0.3) * 100
    score = max(0, min(100, score))
    return round(score, 2)

def generate_nudge(neura_score, recent_blink_count, last_session_len_sec):
    if neura_score > 80:
        return "Excellent focus. Keep the momentum — try a 15-min deep session."
    if recent_blink_count > 6:
        return "Eyes look tired. Take a 2-min eye rest and stretch."
    if neura_score < 40 and last_session_len_sec > 1800:
        return "You're low on focus after long session. Try a 3-min reset."
    if neura_score < 60:
        return "Lost focus — switch to 10-min micro-practice on an easier topic."
    return "Keep going — short breaks help retention. Consider a 3-min reset now."
