import argparse
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import PLATFORMS
from src.text_generator import generate_feed_caption, generate_story_text
from src.image_generator import generate_image_from_topic
from src.publishers.instagram import post_to_instagram, post_story_to_instagram
from src.publishers.facebook import post_to_facebook
from src.branding import add_watermark, add_logo
from src.text_overlay import add_text_overlay
from src.scheduler import schedule_post, get_pending_posts, mark_as_done, listScheduled_posts, cancel_post
from src.reels import generate_reels_script, generate_reels_caption
from src.best_time import get_best_times, suggest_next_post_time
from src.carousel import generate_carousel
from src.hashtags import research_hashtags, get_hashtag_sets
from src.url_content import generate_post_from_url
from src.ab_testing import generate_variants, compare_captions
from src.repurpose import repurpose_content, generate_multi_format
from src.content_calendar import generate_weekly_plan, generate_monthly_plan, list_calendar, clear_calendar
from src.auto_reply import generate_reply, generate_reply_set, classify_comment, generate_smart_replies
from src.stories_interactive import generate_poll, generate_quiz, generate_sliders, generate_question_box
from src.bg_remover import remove_background_simple, change_background, create_gradient_bg
from src.batch import generate_batch, generate_week_batch
from src.templates import get_template, generate_niche_post, list_niches, NICHES
from src.competitor import analyze_competitor, generate_competitor_content, find_competitors
from src.multilang import translate_caption, translate_batch, create_multilingual_post, get_supported_languages


def cmd_post(args):
    print(f"\n{'='*50}")
    print("CRIANDO POST")
    print(f"{'='*50}")

    print("[1/5] Gerando legenda...")
    caption = generate_feed_caption(args.topic, args.tone)
    print(f"Legenda:\n{caption}\n")

    print("[2/5] Gerando textos para stories...")
    stories = generate_story_text(args.topic, args.tone)
    print(f"Stories:\n{stories}\n")

    print("[3/5] Gerando imagem...")
    image_path = generate_image_from_topic(args.topic)
    print(f"Imagem: {image_path}\n")

    if args.watermark:
        print("[4/5] Adicionando marca d'agua...")
        image_path = add_watermark(image_path, text=args.watermark)
    elif args.logo:
        print("[4/5] Adicionando logo...")
        image_path = add_logo(image_path, logo_path=args.logo)

    if args.text_overlay:
        print("[4/5] Adicionando texto sobre imagem...")
        image_path = add_text_overlay(image_path, text=args.text_overlay)

    print("[5/5] Publicando...")
    results = {}

    for platform in args.platforms:
        if not PLATFORMS.get(platform, {}).get("enabled"):
            print(f"AVISO: {platform} nao configurado. Pulando...")
            continue
        try:
            if platform == "instagram":
                post_to_instagram(image_path, caption)
                post_story_to_instagram(image_path)
                results[platform] = "Sucesso"
            elif platform == "facebook":
                post_to_facebook(image_path, caption)
                results[platform] = "Sucesso"
        except Exception as e:
            results[platform] = f"Erro: {e}"

    print(f"\nResultado: {results}")
    return results


def cmd_schedule(args):
    print(f"\nAgendando post para: {args.time}")
    post = schedule_post(
        topic=args.topic,
        platforms=args.platforms,
        scheduled_time=args.time,
        tone=args.tone,
    )
    print(f"Post agendado com ID: {post['id']}")
    return post


def cmd_reels(args):
    print(f"\n{'='*50}")
    print("ROTEIRO PARA REELS/TIKTOK")
    print(f"{'='*50}")

    script = generate_reels_script(args.topic, args.duration, args.tone)
    print(f"\nGANCHO: {script.get('hook', '')}")
    print(f"DESENVOLVIMENTO: {script.get('development', '')}")
    print(f"CTA: {script.get('cta', '')}")
    print(f"\nVISUAL: {script.get('visual', '')}")
    print(f"MUSICA: {script.get('music', '')}")
    print(f"LEGENDAS: {script.get('subtitles', '')}")

    caption = generate_reels_caption(args.topic, args.tone)
    print(f"\nLEGENDA: {caption}")
    return script


def cmd_carousel(args):
    print(f"\n{'='*50}")
    print("CARROSSEL AUTOMATICO")
    print(f"{'='*50}")

    result = generate_carousel(args.topic, args.slides)
    print(f"\nTotal de slides: {result['total_slides']}")
    for slide in result["slides"]:
        print(f"  Slide {slide['number']}: {slide['title']}")
    return result


def cmd_hashtags(args):
    print(f"\n{'='*50}")
    print("PESQUISA DE HASHTAGS")
    print(f"{'='*50}")

    hashtags = research_hashtags(args.topic, count=args.count)
    if args.sets:
        print("\nConjuntos por nivel:")
        get_hashtag_sets(args.topic)
    return hashtags


def cmd_url(args):
    print(f"\n{'='*50}")
    print("CONTEUDO A PARTIR DE URL")
    print(f"{'='*50}")

    result = generate_post_from_url(args.url, args.tone)
    print(f"\n{result['generated_content']}")
    return result


def cmd_besttime(args):
    print(f"\n{'='*50}")
    print("MELHORES HORARIOS")
    print(f"{'='*50}")

    times = get_best_times(args.platform)
    next_time = suggest_next_post_time(args.platform)
    print(f"\nProximo horario ideal: {next_time}")
    return times


def cmd_list_schedule(args):
    print(f"\n{'='*50}")
    print("POSTS AGENDADOS")
    print(f"{'='*50}")

    posts = listScheduled_posts()
    if not posts:
        print("Nenhum post agendado.")
    for post in posts:
        print(f"  ID: {post['id']} | {post['scheduled_time']} | {post['topic']}")
    return posts


def cmd_cancel(args):
    cancel_post(args.id)


def cmd_abtest(args):
    print(f"\n{'='*50}")
    print("A/B TESTING DE LEGENDAS")
    print(f"{'='*50}")

    if args.compare:
        result = compare_captions(args.variant_a, args.variant_b)
        return result
    else:
        variants = generate_variants(args.topic, args.variants, args.tone)
        return variants


def cmd_repurpose(args):
    print(f"\n{'='*50}")
    print("REAPROVEITAR CONTEUDO")
    print(f"{'='*50}")

    if args.original:
        result = repurpose_content(args.topic, args.original)
    else:
        result = generate_multi_format(args.topic)
    return result


def cmd_calendar(args):
    print(f"\n{'='*50}")
    print("CALENDARIO DE CONTEUDO")
    print(f"{'='*50}")

    if args.action == "weekly":
        plan = generate_weekly_plan(args.niche, args.days)
        return plan
    elif args.action == "monthly":
        plan = generate_monthly_plan(args.niche)
        return plan
    elif args.action == "list":
        cal = list_calendar()
        print(f"Posts agendados: {len(cal.get('posts', []))}")
        return cal
    elif args.action == "clear":
        clear_calendar()


def cmd_reply(args):
    print(f"\n{'='*50}")
    print("AUTO-RESPOSTA COMENTARIOS")
    print(f"{'='*50}")

    if args.smart:
        comments = [c.strip() for c in args.comments.split("|")]
        results = generate_smart_replies(comments)
        return results
    elif args.classify:
        category = classify_comment(args.comment)
        print(f"Comentario: {args.comment}")
        print(f"Categoria: {category}")
        return category
    else:
        reply = generate_reply(args.comment, args.tone)
        print(f"Comentario: {args.comment}")
        print(f"Resposta: {reply}")
        return reply


def cmd_stories(args):
    print(f"\n{'='*50}")
    print("STORIES INTERATIVOS")
    print(f"{'='*50}")

    if args.type == "poll":
        return generate_poll(args.topic)
    elif args.type == "quiz":
        return generate_quiz(args.topic)
    elif args.type == "sliders":
        return generate_sliders(args.topic)
    elif args.type == "questions":
        return generate_question_box(args.topic)
    else:
        return generate_poll(args.topic)


def cmd_bg(args):
    print(f"\n{'='*50}")
    print("REMOVER/MUDAR FUNDO")
    print(f"{'='*50}")

    if args.action == "remove":
        return remove_background_simple(args.image, args.output, args.threshold)
    elif args.action == "change":
        color = tuple(int(x) for x in args.color.split(","))
        return change_background(args.image, color, args.output)
    elif args.action == "gradient":
        return create_gradient_bg(output_path=args.output or "gradient.png")


def cmd_batch(args):
    print(f"\n{'='*50}")
    print("LOTE DE POSTS")
    print(f"{'='*50}")

    if args.week:
        result = generate_week_batch(args.niche, args.watermark)
    else:
        topics = [t.strip() for t in args.topics.split("|")]
        result = generate_batch(topics, args.watermark)
    return result


def cmd_templates(args):
    print(f"\n{'='*50}")
    print("TEMPLATES POR NICHO")
    print(f"{'='*50}")

    if args.action == "list":
        list_niches()
    elif args.action == "get":
        return get_template(args.niche)
    elif args.action == "post":
        return generate_niche_post(args.niche, args.topic, args.tone)


def cmd_competitor(args):
    print(f"\n{'='*50}")
    print("ANALISE DE CONCORRENTES")
    print(f"{'='*50}")

    if args.find:
        return find_competitors(args.niche)
    elif args.content:
        result = analyze_competitor(args.username)
        return generate_competitor_content(result["analysis"], args.topic)
    else:
        return analyze_competitor(args.username)


def cmd_translate(args):
    print(f"\n{'='*50}")
    print("LEGENDAS MULTI-IDIOMA")
    print(f"{'='*50}")

    if args.languages:
        langs = [l.strip() for l in args.languages.split("|")]
        return translate_batch(args.caption, langs)
    elif args.multilang:
        return create_multilingual_post(args.topic)
    else:
        return translate_caption(args.caption, args.target_lang)


def main():
    parser = argparse.ArgumentParser(
        description="Automacao completa de redes sociais com IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Comandos disponiveis:
  post         Criar e publicar post completo
  schedule     Agendar post para horario especifico
  reels        Gerar roteiro para Reels/TikTok
  carousel     Gerar carrossel automatico
  hashtags     Pesquisar hashtags trending
  url          Gerar conteudo a partir de URL
  besttime     Melhores horarios para postar
  list         Listar posts agendados
  cancel       Cancelar post agendado
  abtest       A/B Testing de legendas
  repurpose    Reaproveitar conteudo em multiplas plataformas
  calendar     Calendario de conteudo semanal/mensal
  reply        Auto-resposta para comentarios
  stories      Gerar stories interativos (enquete, quiz, etc.)
  bg           Remover ou trocar fundo de imagens
  batch        Gerar lote de posts de uma vez
  templates    Templates prontos por nicho
  competitor   Analise de concorrentes
  translate    Legendas multi-idioma
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos")

    p_post = subparsers.add_parser("post", help="Criar e publicar post")
    p_post.add_argument("topic", help="Topico/tema")
    p_post.add_argument("-p", "--platforms", nargs="+", default=["instagram"])
    p_post.add_argument("-t", "--tone", default="profissional")
    p_post.add_argument("--watermark", help="Marca d'agua (texto)")
    p_post.add_argument("--logo", help="Caminho do logo")
    p_post.add_argument("--text-overlay", help="Texto sobre a imagem")

    p_schedule = subparsers.add_parser("schedule", help="Agendar post")
    p_schedule.add_argument("topic", help="Topico/tema")
    p_schedule.add_argument("time", help="Data/hora: YYYY-MM-DD HH:MM")
    p_schedule.add_argument("-p", "--platforms", nargs="+", default=["instagram"])
    p_schedule.add_argument("-t", "--tone", default="profissional")

    p_reels = subparsers.add_parser("reels", help="Roteiro para Reels")
    p_reels.add_argument("topic", help="Topico/tema")
    p_reels.add_argument("--duration", type=int, default=30)
    p_reels.add_argument("-t", "--tone", default="casual")

    p_carousel = subparsers.add_parser("carousel", help="Carrossel automatico")
    p_carousel.add_argument("topic", help="Topico/tema")
    p_carousel.add_argument("--slides", type=int, default=5)

    p_hashtags = subparsers.add_parser("hashtags", help="Pesquisar hashtags")
    p_hashtags.add_argument("topic", help="Topico/tema")
    p_hashtags.add_argument("--count", type=int, default=15)
    p_hashtags.add_argument("--sets", action="store_true")

    p_url = subparsers.add_parser("url", help="Conteudo de URL")
    p_url.add_argument("url", help="URL do artigo")
    p_url.add_argument("-t", "--tone", default="profissional")

    p_besttime = subparsers.add_parser("besttime", help="Melhores horarios")
    p_besttime.add_argument("-p", "--platform", default="instagram")

    p_list = subparsers.add_parser("list", help="Listar agendamentos")
    p_cancel = subparsers.add_parser("cancel", help="Cancelar agendamento")
    p_cancel.add_argument("id", type=int)

    p_abtest = subparsers.add_parser("abtest", help="A/B Testing de legendas")
    p_abtest.add_argument("topic", nargs="?", help="Topico (para gerar variantes)")
    p_abtest.add_argument("--variants", type=int, default=3)
    p_abtest.add_argument("--compare", action="store_true")
    p_abtest.add_argument("--variant-a", help="Legenda A (para comparar)")
    p_abtest.add_argument("--variant-b", help="Legenda B (para comparar)")
    p_abtest.add_argument("-t", "--tone", default="profissional")

    p_repurpose = subparsers.add_parser("repurpose", help="Reaproveitar conteudo")
    p_repurpose.add_argument("topic", help="Topico/tema")
    p_repurpose.add_argument("--original", help="Legenda original")
    p_repurpose.add_argument("--full", action="store_true", help="Gerar multi-formato com imagens")

    p_calendar = subparsers.add_parser("calendar", help="Calendario de conteudo")
    p_calendar.add_argument("action", choices=["weekly", "monthly", "list", "clear"])
    p_calendar.add_argument("--niche", help="Nicho")
    p_calendar.add_argument("--days", type=int, default=7)

    p_reply = subparsers.add_parser("reply", help="Auto-resposta comentarios")
    p_reply.add_argument("--comment", help="Comentario para responder")
    p_reply.add_argument("--comments", help="Multiplas separadas por |")
    p_reply.add_argument("--smart", action="store_true", help="Resposta inteligente com classificacao")
    p_reply.add_argument("--classify", action="store_true", help="Classificar comentario")
    p_reply.add_argument("-t", "--tone", default="amigavel")

    p_stories = subparsers.add_parser("stories", help="Stories interativos")
    p_stories.add_argument("topic", help="Topico/tema")
    p_stories.add_argument("--type", choices=["poll", "quiz", "sliders", "questions"], default="poll")

    p_bg = subparsers.add_parser("bg", help="Remover/mudar fundo")
    p_bg.add_argument("action", choices=["remove", "change", "gradient"])
    p_bg.add_argument("--image", help="Caminho da imagem")
    p_bg.add_argument("--output", help="Caminho de saida")
    p_bg.add_argument("--threshold", type=int, default=240)
    p_bg.add_argument("--color", help="Cor RGB: 255,255,255")

    p_batch = subparsers.add_parser("batch", help="Lote de posts")
    p_batch.add_argument("--topics", help="Temas separados por |")
    p_batch.add_argument("--week", action="store_true", help="Gerar lote semanal")
    p_batch.add_argument("--niche", help="Nicho (para lote semanal)")
    p_batch.add_argument("--watermark", help="Marca d'agua")

    p_templates = subparsers.add_parser("templates", help="Templates por nicho")
    p_templates.add_argument("action", choices=["list", "get", "post"])
    p_templates.add_argument("--niche", help="Nome do nicho")
    p_templates.add_argument("--topic", help="Topico especifico")
    p_templates.add_argument("-t", "--tone", default=None)

    p_competitor = subparsers.add_parser("competitor", help="Analise de concorrentes")
    p_competitor.add_argument("--username", help="Username do concorrente")
    p_competitor.add_argument("--niche", help="Nicho para buscar concorrentes")
    p_competitor.add_argument("--find", action="store_true", help="Encontrar concorrentes")
    p_competitor.add_argument("--content", action="store_true", help="Gerar conteudo inspirado")
    p_competitor.add_argument("--topic", help="Topico para conteudo")

    p_translate = subparsers.add_parser("translate", help="Legendas multi-idioma")
    p_translate.add_argument("--caption", help="Legenda para traduzir")
    p_translate.add_argument("--target-lang", default="en", help="Idioma alvo (pt, en, es, fr...)")
    p_translate.add_argument("--languages", help="Multiplas traducoes: en|es|fr")
    p_translate.add_argument("--multilang", action="store_true", help="Post em multiplas linguas")
    p_translate.add_argument("--topic", help="Topico (para post multilingue)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        "post": cmd_post,
        "schedule": cmd_schedule,
        "reels": cmd_reels,
        "carousel": cmd_carousel,
        "hashtags": cmd_hashtags,
        "url": cmd_url,
        "besttime": cmd_besttime,
        "list": cmd_list_schedule,
        "cancel": cmd_cancel,
        "abtest": cmd_abtest,
        "repurpose": cmd_repurpose,
        "calendar": cmd_calendar,
        "reply": cmd_reply,
        "stories": cmd_stories,
        "bg": cmd_bg,
        "batch": cmd_batch,
        "templates": cmd_templates,
        "competitor": cmd_competitor,
        "translate": cmd_translate,
    }

    func = commands.get(args.command)
    if func:
        func(args)


if __name__ == "__main__":
    main()
